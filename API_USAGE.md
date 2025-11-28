# Creating Jenkins Pipelines via API

This guide shows how to create Jenkins pipeline jobs dynamically using:
1. **Ansible** (Recommended - cleanest approach)
2. Jenkins REST API (Python/Bash/curl scripts)
3. Job DSL Plugin

## Method 0: Using Ansible (Recommended) ⭐

The cleanest way to create Jenkins jobs is using Ansible's `community.general.jenkins_job` module. It's idempotent, handles errors well, and integrates with your existing Ansible infrastructure.

### Prerequisites:
```bash
# Install the collection (if not already installed)
ansible-galaxy collection install community.general
```

### Quick Start:
```bash
export JENKINS_TOKEN="your-token"
export JOB_NAME="coffee_order_pipeline"
export JENKINSFILE_PATH="../Jenkinsfile"

ansible-playbook playbooks/create_jenkins_pipeline.yml
```

### From JSON Config:
```bash
export JENKINS_TOKEN="your-token"
export JSON_CONFIG_FILE="../pipeline_config.json"

ansible-playbook playbooks/create_jenkins_pipeline_from_json.yml
```

### Manage Jobs (Create/Delete/Enable/Disable):
```bash
# Create job
JOB_ACTION=create ansible-playbook playbooks/manage_jenkins_job.yml

# Delete job
JOB_ACTION=delete ansible-playbook playbooks/manage_jenkins_job.yml

# Disable job
JOB_ACTION=disable ansible-playbook playbooks/manage_jenkins_job.yml

# Enable job
JOB_ACTION=enable ansible-playbook playbooks/manage_jenkins_job.yml
```

### Benefits of Ansible Approach:
- ✅ **Idempotent** - Safe to run multiple times
- ✅ **Error handling** - Better error messages
- ✅ **Version control** - Playbooks are version controlled
- ✅ **Integration** - Works with existing Ansible infrastructure
- ✅ **Check mode** - Test changes without applying (`--check`)
- ✅ **Documentation** - Self-documenting playbooks

### Reference:
- [Ansible Jenkins Job Module Documentation](https://docs.ansible.com/projects/ansible/latest/collections/community/general/jenkins_job_module.html)

## Prerequisites

1. **Get Your Jenkins API Token:**
   - Go to Jenkins → Click your username (top right)
   - Click **Configure**
   - Under **API Token**, click **Add new Token**
   - Give it a name (e.g., "api-token")
   - Click **Generate**
   - **Copy the token** (you won't see it again!)

2. **Set Environment Variables:**
   ```bash
   export JENKINS_URL="http://localhost:8080"
   export JENKINS_USER="zhaq"  # or your Jenkins username
   export JENKINS_TOKEN="your-api-token-here"
   ```

## Method 1: Using Bash Script (Direct)

### Usage:
```bash
chmod +x create_pipeline.sh
./create_pipeline.sh <job-name> <jenkinsfile-path>
```

### Example:
```bash
./create_pipeline.sh coffee_order_pipeline Jenkinsfile
```

## Method 2: Using Python Script (Direct)

### Usage:
```bash
python3 create_pipeline.py <job-name> <jenkinsfile-path>
```

### Example:
```bash
python3 create_pipeline.py coffee_order_pipeline Jenkinsfile
```

## Method 3: Using curl Directly

### Create Pipeline from Inline Jenkinsfile:
```bash
JOB_NAME="coffee_order_pipeline"
JENKINSFILE_PATH="Jenkinsfile"
JENKINS_URL="http://localhost:8080"
JENKINS_USER="admin"
JENKINS_TOKEN="your-token"

# Read and escape Jenkinsfile
JENKINSFILE_CONTENT=$(cat "$JENKINSFILE_PATH" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

# Create XML config
CONFIG_XML="<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin=\"workflow-job@2.42\">
  <description>Auto-created pipeline</description>
  <keepDependencies>false</keepDependencies>
  <definition class=\"org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition\" plugin=\"workflow-cps@2.92\">
    <script>${JENKINSFILE_CONTENT}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>"

# Create job
curl -X POST \
  "${JENKINS_URL}/createItem?name=${JOB_NAME}" \
  --user "${JENKINS_USER}:${JENKINS_TOKEN}" \
  --data-binary "${CONFIG_XML}" \
  --header "Content-Type: application/xml"
```

## Method 4: Create Pipeline from Git Repository

### Using Python with python-jenkins library:
```bash
pip install python-jenkins
python3 create_pipeline_advanced.py coffee_pipeline https://github.com/user/repo.git main Jenkinsfile
```

## API Endpoints Reference

### Create Job:
```
POST /createItem?name=<job-name>
Content-Type: application/xml
```

### Update Job:
```
POST /job/<job-name>/config.xml
Content-Type: application/xml
```

### Get Job Config:
```
GET /job/<job-name>/config.xml
```

### Delete Job:
```
POST /job/<job-name>/doDelete
```

### Build Job:
```
POST /job/<job-name>/build
```

### Get Build Status:
```
GET /job/<job-name>/lastBuild/api/json
```

## Example: Complete Workflow

```bash
#!/bin/bash
# Complete workflow: Create, build, and monitor pipeline

JOB_NAME="coffee_order_pipeline"
JENKINS_URL="http://localhost:8080"
JENKINS_USER="admin"
JENKINS_TOKEN="your-token"

# 1. Create the pipeline
./create_pipeline.sh "$JOB_NAME" Jenkinsfile

# 2. Trigger a build
curl -X POST \
  "${JENKINS_URL}/job/${JOB_NAME}/build" \
  --user "${JENKINS_USER}:${JENKINS_TOKEN}"

# 3. Wait for build to start
sleep 5

# 4. Get build status
curl -s \
  "${JENKINS_URL}/job/${JOB_NAME}/lastBuild/api/json" \
  --user "${JENKINS_USER}:${JENKINS_TOKEN}" | \
  python3 -m json.tool
```

## Using Jenkins Python Library

```python
import jenkins

server = jenkins.Jenkins(
    'http://localhost:8080',
    username='admin',
    password='your-api-token'
)

# Create job from config XML
with open('job_config.xml', 'r') as f:
    config_xml = f.read()

server.create_job('my_pipeline', config_xml)

# Build the job
server.build_job('my_pipeline')

# Get job info
job_info = server.get_job_info('my_pipeline')
print(job_info)
```

## Troubleshooting

### Authentication Issues:
- Make sure your API token is correct
- Check that your user has permission to create jobs
- Try using username:password instead of username:token

### Job Already Exists:
- Delete existing job first: `POST /job/<name>/doDelete`
- Or update it: `POST /job/<name>/config.xml`

### XML Errors:
- Validate your XML before sending
- Check Jenkins logs for detailed error messages

## Security Notes

- Never commit API tokens to version control
- Use environment variables or secret management
- Rotate tokens regularly
- Use least-privilege access

