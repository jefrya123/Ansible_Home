pipeline {
    agent { label 'ansible' }  // Ensures this runs on the agent with Ansible installed
    triggers {
        githubPush()  // Trigger pipeline on GitHub push events
    }
    stages {
        stage('Pull Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/jefrya123/Ansible_Home.git'
            }
        }
        stage('Run Ansible Playbook') {
            steps {
                script {
                    sh '''
                    ansible-playbook -i inventory.yml playbooks/site.yml
                    '''
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
