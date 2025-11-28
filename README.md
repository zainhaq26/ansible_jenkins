# Ansible Jenkins Integration

This repository demonstrates how to use **Ansible** to manage Jenkins pipelines and integrate with external APIs. It provides a complete example of automating Jenkins job creation, build management, and API interactions.

## What This Repository Does

This repository contains:

1. **Ansible Playbooks for Jenkins Management**
   - Create, delete, enable, and disable Jenkins pipeline jobs
   - Trigger, stop, and delete Jenkins builds
   - All using Ansible's `community.general` collection modules

2. **Coffee Shop API Integration**
   - Ansible playbooks to interact with a [coffee shop API](https://github.com/zainhaq26/coffee_shop)
   - Order coffee with customizable options
   - Retrieve order details and list all orders

3. **Jenkins Pipeline Automation**
   - A Jenkins pipeline that uses Ansible to:
     - Place a coffee order
     - Retrieve the order details
   - Demonstrates CI/CD integration with Ansible

4. **Jenkins Pipeline Creation Scripts**
   - Python and Bash scripts to create Jenkins pipelines via REST API
   - Support for JSON configuration files
   - Examples of programmatic Jenkins job creation

## Repository Structure

```
ansible_jenkins/
├── playbooks/
│   ├── manage_jenkins_job.yml          # Create/delete/enable/disable Jenkins jobs
│   ├── manage_jenkins_build.yml         # Trigger/stop/delete Jenkins builds
│   ├── create_jenkins_pipeline.yml      # Create pipeline from Jenkinsfile
│   ├── create_jenkins_pipeline_from_json.yml  # Create pipeline from JSON config
│   ├── order_coffee.yml                 # Order coffee via API
│   └── get_orders.yml                   # Get coffee orders via API
├── scripts/
│   ├── create_pipeline.py               # Create Jenkins pipeline via REST API
│   ├── create_pipeline.sh               # Bash script for pipeline creation
│   └── create_pipeline_advanced.py      # Advanced pipeline creation from Git
├── Jenkinsfile                          # Jenkins pipeline definition
├── pipeline_config.json                 # Example JSON configuration
├── ansible.cfg                          # Ansible configuration
├── inventory/                           # Ansible inventory files
├── ANSIBLE_USAGE.md                     # Detailed Ansible usage guide
└── API_USAGE.md                         # Jenkins REST API usage guide
```

## Key Features

### 🎯 Jenkins Job Management
- **Create pipelines** from Jenkinsfile or JSON config
- **Delete, enable, disable** Jenkins jobs
- **Idempotent operations** - safe to run multiple times
- **Error handling** and validation

### 🚀 Build Management
- **Trigger builds** with optional parameters
- **Stop running builds**
- **Delete completed builds**
- **Detached mode** - don't wait for build completion

### ☕ Coffee Shop API Integration
- **Place coffee orders** with full customization via the [Coffee Shop API](https://github.com/zainhaq26/coffee_shop)
- **Retrieve order details** by ID
- **List all orders** with summaries
- **Automatic conversation grouping** (for messaging service)

### 🔄 Jenkins Pipeline Automation
- **Automated workflow** that orders coffee and retrieves details
- **Ansible integration** within Jenkins pipelines
- **Error handling** and status reporting

## Quick Start

### Prerequisites

1. **Ansible** installed
2. **Jenkins** running (default: `http://localhost:8080`)
3. **[Coffee Shop API](https://github.com/zainhaq26/coffee_shop)** running (default: `http://localhost:8000`)
4. **Ansible Collections:**
   ```bash
   ansible-galaxy collection install community.general
   ```

### Setup

1. **Get Jenkins API Token:**
   - Go to Jenkins → Your Username → Configure
   - Create an API token

2. **Set Environment Variables:**
   ```bash
   export JENKINS_URL="http://localhost:8080"
   export JENKINS_USER="your-username"
   export JENKINS_TOKEN="your-api-token"
   ```

### Examples

**Create a Jenkins Pipeline:**
```bash
ansible-playbook playbooks/manage_jenkins_job.yml \
  -e "job_name=my_pipeline" \
  -e "job_action=create"
```

**Trigger a Build:**
```bash
ansible-playbook playbooks/manage_jenkins_build.yml \
  -e "job_name=my_pipeline" \
  -e "build_action=trigger"
```

**Order Coffee:**
```bash
ansible-playbook playbooks/order_coffee.yml
```

**Get Orders:**
```bash
ansible-playbook playbooks/get_orders.yml
```

## Documentation

- **[ANSIBLE_USAGE.md](ANSIBLE_USAGE.md)** - Complete guide for using Ansible playbooks
- **[API_USAGE.md](API_USAGE.md)** - Guide for creating Jenkins pipelines via REST API

## Use Cases

1. **Infrastructure as Code** - Manage Jenkins jobs declaratively with Ansible
2. **CI/CD Automation** - Automate pipeline creation and management
3. **API Integration** - Demonstrate Ansible's ability to interact with REST APIs
4. **Learning Example** - Understand Ansible-Jenkins integration patterns

## Technologies Used

- **Ansible** - Automation and configuration management
- **Jenkins** - CI/CD platform
- **FastAPI** - [Coffee Shop API](https://github.com/zainhaq26/coffee_shop) (external service)
- **Python** - Scripting and automation
- **YAML** - Configuration and playbook definitions

## Requirements

- Python 3.9+
- Ansible 2.9+
- Jenkins 2.x
- `community.general` Ansible collection
- `python-jenkins` library (for Ansible modules)

## License

This is a demonstration/learning project.
