pipeline {
    agent {
        docker {
            image 'nikolaik/python-nodejs:python3.7-nodejs14-alpine'
            args '-p 3000:3000 -p 5000:5000'
        }
    }
    environment {
        HOME = '.'
        CI = 'true' 
    }
    stages {
        stage('Build FrontEnd') {
            steps {
                dir('react-app') {
                    sh 'npm install'
                }
            }
        }
    }
}