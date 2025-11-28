#!/usr/bin/env python3
"""
Advanced example: Create Jenkins pipeline from Git repository
Requires: pip install python-jenkins
"""

import jenkins
import os
import sys

def create_pipeline_from_git(jenkins_url, job_name, git_url, branch='main', jenkinsfile_path='Jenkinsfile'):
    """Create a Jenkins pipeline job that pulls from Git"""
    
    username = os.getenv('JENKINS_USER', 'admin')
    api_token = os.getenv('JENKINS_TOKEN')
    
    if not api_token:
        print("Error: JENKINS_TOKEN environment variable not set")
        return False
    
    # Connect to Jenkins
    server = jenkins.Jenkins(jenkins_url, username=username, password=api_token)
    
    # Pipeline script (pulls from Git)
    pipeline_script = f"""
pipeline {{
    agent any
    
    stages {{
        stage('Checkout') {{
            steps {{
                checkout scm: [
                    $class: 'GitSCM',
                    branches: [[name: '*/{branch}']],
                    userRemoteConfigs: [[url: '{git_url}']]
                ]
            }}
        }}
        
        stage('Build') {{
            steps {{
                script {{
                    def jenkinsfile = readFile('{jenkinsfile_path}')
                    load jenkinsfile
                }}
            }}
        }}
    }}
}}
"""
    
    # Alternative: Create pipeline that uses Jenkinsfile from SCM
    config_xml = f"""<?xml version='1.1' encoding='UTF-8'?>
<org.jenkinsci.plugins.workflow.job.WorkflowJob plugin="workflow-job@2.42">
  <description>Pipeline from Git: {git_url}</description>
  <keepDependencies>false</keepDependencies>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps@2.92">
    <scm class="hudson.plugins.git.GitSCM" plugin="git@4.8.0">
      <configVersion>2</configVersion>
      <userRemoteConfigs>
        <hudson.plugins.git.UserRemoteConfig>
          <url>{git_url}</url>
        </hudson.plugins.git.UserRemoteConfig>
      </userRemoteConfigs>
      <branches>
        <hudson.plugins.git.BranchSpec>
          <name>*/{branch}</name>
        </hudson.plugins.git.BranchSpec>
      </branches>
      <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
      <submoduleCfg class="list"/>
      <extensions/>
    </scm>
    <scriptPath>{jenkinsfile_path}</scriptPath>
    <lightweight>true</lightweight>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</org.jenkinsci.plugins.workflow.job.WorkflowJob>"""
    
    try:
        # Check if job exists
        try:
            server.get_job_config(job_name)
            print(f"Job '{job_name}' already exists. Updating...")
            server.reconfig_job(job_name, config_xml)
            print(f"✅ Job '{job_name}' updated successfully!")
        except jenkins.NotFoundException:
            print(f"Creating new job '{job_name}'...")
            server.create_job(job_name, config_xml)
            print(f"✅ Job '{job_name}' created successfully!")
        
        print(f"View it at: {jenkins_url}/job/{job_name}/")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python create_pipeline_advanced.py <job-name> <git-url> [branch] [jenkinsfile-path]")
        print("Example: python create_pipeline_advanced.py coffee_pipeline https://github.com/user/repo.git main Jenkinsfile")
        sys.exit(1)
    
    job_name = sys.argv[1]
    git_url = sys.argv[2]
    branch = sys.argv[3] if len(sys.argv) > 3 else 'main'
    jenkinsfile_path = sys.argv[4] if len(sys.argv) > 4 else 'Jenkinsfile'
    
    jenkins_url = os.getenv('JENKINS_URL', 'http://localhost:8080')
    
    success = create_pipeline_from_git(jenkins_url, job_name, git_url, branch, jenkinsfile_path)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

