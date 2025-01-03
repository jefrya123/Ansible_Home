pipeline {
    agent { label 'ansible' }
    triggers {
        githubPush()
    }
    stages {
        stage('Pull Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/jefrya123/Ansible_Home.git'
            }
        }
        stage('Run Ansible Playbook') {
            steps {
                sh '''
                ansible-playbook -i inventories/inventory.yml playbooks/site.yml
                '''
            }
        }
    }
}
