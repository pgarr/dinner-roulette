pipeline {
    agent {
        docker {
            image 'nikolaik/python-nodejs:python3.7-nodejs14-alpine'
            args '-p 3000:3000 -p 5000:5000'
        }
    }
    environment {
        HOME = '${WORKSPACE}'
        CI = 'true' 
        NPM_CONFIG_CACHE = '${WORKSPACE}/.npm'
    }
    stages {
        stage('Build FrontEnd') {
            steps {
                sh 'pwd'
                dir('react-app') {
                sh 'pwd'
                    sh 'npm install'
                }
            }
        }
    }
}