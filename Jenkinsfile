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
        APP_ADMINS='admin'
        FLASK_ENV='development'
    }
    stages {
        stage('Build Backend') {
            steps {
                dir('Jenkinsscripts') {
                    sh 'python make_requirements.py'
                }
                dir('flask-app') {
                    sh 'pip install -r requirements-jenkins.txt'
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