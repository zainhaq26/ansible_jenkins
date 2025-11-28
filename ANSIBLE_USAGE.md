# Creating Jenkins Pipelines with Ansible

This is the **recommended approach** for creating Jenkins pipeline jobs. It uses Ansible's `community.general.jenkins_job` module, which is cleaner, more reliable, and integrates better with infrastructure automation.

## Quick Start

### 1. Set Environment Variables
```bash
export JENKINS_URL="http://localhost:8080"
export JENKINS_USER="zhaq"  # or your Jenkins username
export JENKINS_TOKEN="your-api-token-here"
```

### 2. Create Pipeline from Jenkinsfile
```bash
export JOB_NAME="coffee_order_pipeline"
export JENKINSFILE_PATH="../Jenkinsfile"

ansible-playbook playbooks/create_jenkins_pipeline.yml
```

### 3. Create Pipeline from JSON Config
```bash
export JSON_CONFIG_FILE="../pipeline_config.json"

ansible-playbook playbooks/create_jenkins_pipeline_from_json.yml
```

## Available Playbooks

### `create_jenkins_pipeline.yml`
Creates a Jenkins pipeline job from a Jenkinsfile.

**Environment Variables:**
- `JOB_NAME` - Name of the Jenkins job (default: `coffee_order_pipeline`)
- `JENKINSFILE_PATH` - Path to Jenkinsfile (default: `../Jenkinsfile`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Example:**
```bash
JOB_NAME="my_pipeline" \
JENKINSFILE_PATH="/path/to/Jenkinsfile" \
ansible-playbook playbooks/create_jenkins_pipeline.yml
```

### `create_jenkins_pipeline_from_json.yml`
Creates a Jenkins pipeline job from a JSON configuration file.

**Environment Variables:**
- `JSON_CONFIG_FILE` - Path to JSON config (default: `../pipeline_config.json`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Example JSON Config:**
```json
{
  "job_name": "coffee_order_pipeline",
  "description": "Coffee order pipeline",
  "jenkinsfile_path": "../Jenkinsfile",
  "sandbox": true
}
```

### `manage_jenkins_job.yml`
Multi-purpose playbook for creating, deleting, enabling, or disabling Jenkins jobs.

**Environment Variables:**
- `JOB_NAME` - Name of the Jenkins job
- `JOB_ACTION` - Action to perform: `create`, `delete`, `enable`, `disable` (default: `create`)
- `JENKINSFILE_PATH` - Path to Jenkinsfile (required for `create`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Examples:**
```bash
# Create a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="create" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Delete a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="delete" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Disable a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="disable" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Enable a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="enable" \
ansible-playbook playbooks/manage_jenkins_job.yml
```

### `manage_jenkins_build.yml`
Multi-purpose playbook for triggering, stopping, or deleting Jenkins builds.

**Environment Variables:**
- `JOB_NAME` - Name of the Jenkins job to build
- `BUILD_ACTION` - Action to perform: `trigger`, `stop`, `delete` (default: `trigger`)
- `BUILD_NUMBER` - Build number (required for `stop` and `delete`)
- `BUILD_ARGS` - JSON string of build parameters (optional)
- `DETACH` - Don't wait for build to complete (default: `false`)
- `TIME_BETWEEN_CHECKS` - Seconds between status checks (default: `10`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Examples:**
```bash
# Trigger a build (waits for completion)
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Trigger a build with parameters
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
BUILD_ARGS='{"COFFEE_SIZE": "large", "COFFEE_TYPE": "iced"}' \
ansible-playbook playbooks/manage_jenkins_build.yml

# Trigger a build in detached mode (don't wait)
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
DETACH="true" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Stop a running build
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="stop" \
BUILD_NUMBER="42" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Delete a build
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="delete" \
BUILD_NUMBER="42" \
ansible-playbook playbooks/manage_jenkins_build.yml
```

**Environment Variables:**
- `JOB_NAME` - Name of the Jenkins job
- `JOB_ACTION` - Action to perform: `create`, `delete`, `enable`, `disable` (default: `create`)
- `JENKINSFILE_PATH` - Path to Jenkinsfile (required for `create`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Examples:**
```bash
# Create a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="create" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Delete a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="delete" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Disable a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="disable" \
ansible-playbook playbooks/manage_jenkins_job.yml

# Enable a job
JOB_NAME="coffee_pipeline" \
JOB_ACTION="enable" \
ansible-playbook playbooks/manage_jenkins_job.yml
```

### `manage_jenkins_build.yml`
Multi-purpose playbook for triggering, stopping, or deleting Jenkins builds.

**Environment Variables:**
- `JOB_NAME` - Name of the Jenkins job to build
- `BUILD_ACTION` - Action to perform: `trigger`, `stop`, `delete` (default: `trigger`)
- `BUILD_NUMBER` - Build number (required for `stop` and `delete`)
- `BUILD_ARGS` - JSON string of build parameters (optional)
- `DETACH` - Don't wait for build to complete (default: `false`)
- `TIME_BETWEEN_CHECKS` - Seconds between status checks (default: `10`)
- `JENKINS_URL` - Jenkins URL (default: `http://localhost:8080`)
- `JENKINS_USER` - Jenkins username (default: `admin`)
- `JENKINS_TOKEN` - Jenkins API token (required)

**Examples:**
```bash
# Trigger a build (waits for completion)
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Trigger a build with parameters
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
BUILD_ARGS='{"COFFEE_SIZE": "large", "COFFEE_TYPE": "iced"}' \
ansible-playbook playbooks/manage_jenkins_build.yml

# Trigger a build in detached mode (don't wait)
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="trigger" \
DETACH="true" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Stop a running build
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="stop" \
BUILD_NUMBER="42" \
ansible-playbook playbooks/manage_jenkins_build.yml

# Delete a build
JOB_NAME="coffee_order_pipeline" \
BUILD_ACTION="delete" \
BUILD_NUMBER="42" \
ansible-playbook playbooks/manage_jenkins_build.yml
```

## Advanced Usage

### Check Mode (Dry Run)
Test what would happen without making changes:
```bash
ansible-playbook --check playbooks/create_jenkins_pipeline.yml
```

### Verbose Output
See detailed execution:
```bash
ansible-playbook -v playbooks/create_jenkins_pipeline.yml
# -vv for more detail
# -vvv for even more detail
```

### Using Ansible Vault for Secrets
Store your Jenkins token securely:
```bash
# Create encrypted variable file
ansible-vault create group_vars/all/vault.yml

# Add to vault.yml:
# jenkins_token: your-token-here

# Use in playbook (update playbook to use vault variable)
ansible-playbook --ask-vault-pass playbooks/create_jenkins_pipeline.yml
```

## Benefits Over REST API

1. **Idempotency** - Safe to run multiple times, only creates if doesn't exist
2. **Error Handling** - Better error messages and handling
3. **Check Mode** - Test changes before applying
4. **Integration** - Works with existing Ansible infrastructure
5. **Version Control** - Playbooks are version controlled
6. **Documentation** - Self-documenting playbooks
7. **Reusability** - Easy to create multiple jobs with variables

## Troubleshooting

### Collection Not Found
```bash
ansible-galaxy collection install community.general
```

### Authentication Failed
- Verify your API token is correct
- Check that your user has permission to create jobs
- Try using username:password instead of token

### Job Already Exists
The playbook will update the existing job. To delete first:
```bash
JOB_ACTION=delete ansible-playbook playbooks/manage_jenkins_job.yml
```

### Jenkinsfile Not Found
Make sure `JENKINSFILE_PATH` points to the correct file:
```bash
export JENKINSFILE_PATH="$(pwd)/Jenkinsfile"
```

## Reference

- [Ansible Jenkins Job Module](https://docs.ansible.com/projects/ansible/latest/collections/community/general/jenkins_job_module.html)
- [Ansible Jenkins Build Module](https://docs.ansible.com/projects/ansible/latest/collections/community/general/jenkins_build_module.html)
- [Ansible Documentation](https://docs.ansible.com/)

