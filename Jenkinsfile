pipeline {
    agent any
    
    environment {
        ANSIBLE_CONFIG = "/Users/zainhaq/Documents/workspace/ansible_jenkins/ansible.cfg"
        COFFEE_SHOP_URL = "http://localhost:8000"
        PLAYBOOKS_DIR = "/Users/zainhaq/Documents/workspace/ansible_jenkins/playbooks"
        INVENTORY_FILE = "/Users/zainhaq/Documents/workspace/ansible_jenkins/inventory/inventory.ini"
        ANSIBLE_BIN = "/opt/homebrew/bin"
        PATH = "/opt/homebrew/bin:${env.PATH}"
    }
    
    stages {

        stage('Debug') {
            steps {
                echo "Playbooks directory: ${env.PLAYBOOKS_DIR}"
                echo "Inventory file: ${env.INVENTORY_FILE}"
                echo "Ansible bin path: ${env.ANSIBLE_BIN}"
                sh 'pwd'
                sh 'whoami'
                sh 'echo $PATH'
                sh 'which ansible-playbook || echo "ansible-playbook not found in PATH"'
                sh "ls -la ${env.PLAYBOOKS_DIR}"
            }
        }
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                // Git checkout would go here if using SCM
            }
        }
        
        stage('Place Coffee Order') {
            steps {
                echo 'Placing coffee order...'
                script {
                    // Run the order coffee playbook using Ansible plugin
                    // Configure Ansible in Jenkins: Manage Jenkins → Tools → Add Ansible
                    // Name: "Ansible", Path: "/opt/homebrew/bin/ansible-playbook"
                    ansiblePlaybook(
                        playbook: "${env.PLAYBOOKS_DIR}/order_coffee.yml",
                        inventory: "${env.INVENTORY_FILE}",
                        extras: '-e "coffee_order.size=medium" -e "coffee_order.coffee_type=hot" -e "coffee_order.milk=oat"',
                        colorized: true,
                        installation: "Ansible"
                    )
                    
                    // Read order ID from file created by Ansible
                    if (fileExists('/tmp/order_id.txt')) {
                        env.ORDER_ID = readFile('/tmp/order_id.txt').trim()
                        echo "✅ Order placed successfully!"
                        echo "📋 Order ID: ${env.ORDER_ID}"
                    } else {
                        error("Failed to create order ID file. Order may not have been placed.")
                    }
                }
            }
        }
        
        stage('Get Order Details') {
            steps {
                echo "Retrieving order details for Order ID: ${env.ORDER_ID}"
                script {
                    ansiblePlaybook(
                        playbook: "${env.PLAYBOOKS_DIR}/get_orders.yml",
                        inventory: "${env.INVENTORY_FILE}",
                        extras: "-e \"order_id=${env.ORDER_ID}\"",
                        colorized: true,
                        installation: "Ansible"
                    )
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully! ☕'
            script {
                if (env.ORDER_ID) {
                    echo "Order ID: ${env.ORDER_ID}"
                }
            }
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}

