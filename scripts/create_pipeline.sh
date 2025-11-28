#!/bin/bash

# Script to create a Jenkins pipeline job via REST API
# Usage: ./create_pipeline.sh <job-name> <jenkinsfile-path>

JENKINS_URL="http://localhost:8080"
JOB_NAME="${1:-coffee_order_pipeline}"
JENKINSFILE_PATH="${2:-Jenkinsfile}"
JENKINS_USER="${JENKINS_USER:-admin}"  # Change if needed
JENKINS_TOKEN="${JENKINS_TOKEN}"  # Get from Jenkins → Manage Jenkins → API Token

if [ -z "$JENKINS_TOKEN" ]; then
    echo "Error: JENKINS_TOKEN environment variable not set"
    echo "Get your API token from: Jenkins → Your Name → Configure → API Token"
    exit 1
fi

# Read Jenkinsfile content
if [ ! -f "$JENKINSFILE_PATH" ]; then
    echo "Error: Jenkinsfile not found at $JENKINSFILE_PATH"
    exit 1
fi

JENKINSFILE_CONTENT=$(cat "$JENKINSFILE_PATH" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')

# Create XML config for pipeline job
CONFIG_XML=$(cat <<EOF
<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.42">
  <description>Automatically created pipeline for coffee orders</description>
  <keepDependencies>false</keepDependencies>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.92">
    <script>${JENKINSFILE_CONTENT}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
EOF
)

# Create the job
echo "Creating Jenkins pipeline job: $JOB_NAME"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    "${JENKINS_URL}/createItem?name=${JOB_NAME}" \
    --user "${JENKINS_USER}:${JENKINS_TOKEN}" \
    --data-binary "${CONFIG_XML}" \
    --header "Content-Type: application/xml")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
    echo "✅ Pipeline job '$JOB_NAME' created successfully!"
    echo "View it at: ${JENKINS_URL}/job/${JOB_NAME}/"
else
    echo "❌ Failed to create job. HTTP Code: $HTTP_CODE"
    echo "Response: $BODY"
    exit 1
fi

