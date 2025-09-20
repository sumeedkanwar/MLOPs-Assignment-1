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

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Lint (Flake8)') {
            steps {
                sh '. venv/bin/activate && flake8 app/ --max-line-length=120'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '. venv/bin/activate && pytest tests/ --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        success {
            mail to: "${ADMIN_EMAIL}",
                 subject: "✅ Jenkins Pipeline Success - Build #${BUILD_NUMBER}",
                 body: "The pipeline for MLOPs Assignment 1 completed successfully.\nDocker Image: ${DOCKER_IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            mail to: "${ADMIN_EMAIL}",
                 subject: "❌ Jenkins Pipeline Failed - Build #${BUILD_NUMBER}",
                 body: "The pipeline failed. Please check Jenkins for logs."
        }
    }
}
