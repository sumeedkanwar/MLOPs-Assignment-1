pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-creds')
        DOCKER_IMAGE = "sumeedkanwar/mlops-assignment-1"
        ADMIN_EMAIL = "sumeedkanwar@gmail.com"
    }


    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sumeedkanwar/MLOPs-Assignment-1.git'
            }
        }

        stage('Lint & Test') {
            agent {
                docker {
                    image 'python:3.10'
                }
            }
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'flake8 app/ --max-line-length=120'
                sh 'pytest tests/ --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
    }


    post {
        success {
            mail to: "${env.ADMIN_EMAIL}",
                 subject: "✅ Jenkins Pipeline Success - Build #${BUILD_NUMBER}",
                 body: "The pipeline completed successfully.\nDocker Image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            mail to: "${env.ADMIN_EMAIL}",
                 subject: "❌ Jenkins Pipeline Failed - Build #${BUILD_NUMBER}",
                 body: "The pipeline failed. Please check Jenkins logs."
        }
    }
}