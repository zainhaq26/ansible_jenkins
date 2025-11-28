#!/usr/bin/env python3
"""
Create a Jenkins pipeline job dynamically using Jenkins REST API
Usage: python create_pipeline.py <job-name> <jenkinsfile-path>
"""

import sys
import os
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_pipeline_job(jenkins_url, job_name, jenkinsfile_path, username, api_token):
    """Create a Jenkins pipeline job from a Jenkinsfile"""
    
    # Read Jenkinsfile
    if not os.path.exists(jenkinsfile_path):
        print(f"Error: Jenkinsfile not found at {jenkinsfile_path}")
        return False
    
    with open(jenkinsfile_path, 'r') as f:
        jenkinsfile_content = f.read()
    
    # Create XML configuration
    root = ET.Element('flow-definition')
    root.set('plugin', 'workflow-job@2.42')
    
    description = ET.SubElement(root, 'description')
    description.text = f'Automatically created pipeline: {job_name}'
    
    keep_deps = ET.SubElement(root, 'keepDependencies')
    keep_deps.text = 'false'
    
    definition = ET.SubElement(root, 'definition')
    definition.set('class', 'org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition')
    definition.set('plugin', 'workflow-cps@2.92')
    
    script = ET.SubElement(definition, 'script')
    script.text = jenkinsfile_content
    
    sandbox = ET.SubElement(definition, 'sandbox')
    sandbox.text = 'true'
    
    triggers = ET.SubElement(root, 'triggers')
    disabled = ET.SubElement(root, 'disabled')
    disabled.text = 'false'
    
    # Convert to XML string
    xml_str = ET.tostring(root, encoding='unicode')
    xml_str = '<?xml version="1.1" encoding="UTF-8"?>\n' + xml_str
    
    # Pretty print
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # Create job via API
    url = f"{jenkins_url}/createItem?name={job_name}"
    headers = {'Content-Type': 'application/xml'}
    auth = (username, api_token)
    
    print(f"Creating Jenkins pipeline job: {job_name}")
    response = requests.post(url, data=pretty_xml, headers=headers, auth=auth)
    
    if response.status_code in [200, 201]:
        print(f"✅ Pipeline job '{job_name}' created successfully!")
        print(f"View it at: {jenkins_url}/job/{job_name}/")
        return True
    else:
        print(f"❌ Failed to create job. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: python create_pipeline.py <job-name> <jenkinsfile-path>")
        print("Example: python create_pipeline.py coffee_order_pipeline Jenkinsfile")
        sys.exit(1)
    
    job_name = sys.argv[1]
    jenkinsfile_path = sys.argv[2]
    
    jenkins_url = os.getenv('JENKINS_URL', 'http://localhost:8080')
    username = os.getenv('JENKINS_USER', 'admin')
    api_token = os.getenv('JENKINS_TOKEN')
    
    if not api_token:
        print("Error: JENKINS_TOKEN environment variable not set")
        print("Get your API token from: Jenkins → Your Name → Configure → API Token")
        sys.exit(1)
    
    success = create_pipeline_job(jenkins_url, job_name, jenkinsfile_path, username, api_token)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

