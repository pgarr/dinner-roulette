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
        stage('Build Backend') {
            steps {
                dir('flask-app') {
                    sh 'pip install -r requirements-tests.txt'
                }
            }
        }
        stage('Build Frontend') {
            steps {
                dir('react-app') {
                    sh 'npm install'
                }
            }
        }
        stage('Test Backend') { 
            steps {
                dir('flask-app') {
                    sh 'python -m pytest'
                }
            }
        }
        stage('Test Frontend') { 
            steps {
                dir('react-app') {
                    sh 'npm test'
                }
            }
        }
    }
}