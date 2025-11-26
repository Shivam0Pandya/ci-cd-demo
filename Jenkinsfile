// Jenkinsfile
pipeline {
    agent any

    environment {
        // !! UPDATE THIS: Replace with your actual Docker Hub username and Roll Number !!
        DOCKER_IMAGE = "imt2023091/ci-cd-demo`"
    }

    stages {
        stage('Pull Code') {
            steps {
                echo "--- Pulling code from GitHub..."
            }
        }

        stage('Test (Pytest in Docker)') {
            steps {
                script {
                    echo "--- Running automated Pytest tests inside a Docker container..."
                    
                    // The 'sh' command runs the tests inside a temporary 'python:3.9-slim' container.
                    // -v "${PWD}":/app mounts the current Jenkins workspace into the container.
                    // -w /app sets the working directory inside the container.
                    // /bin/bash -c "..." chains the dependency installation and the test command.
                    sh '''
                        docker run --rm \
                        -v "${PWD}":/app \
                        -w /app \
                        python:3.10-slim /bin/bash -c "pip install -r requirements.txt && python -m pytest test_calculator.py"
                    '''
                    
                    echo "Tests passed successfully in isolated Docker environment!"
                }
            }
        }

        stage('Create Docker Image') {
            steps {
                echo "--- Building final Docker image: ${env.DOCKER_IMAGE}:latest"
                // This uses the Dockerfile in your workspace to build the final image
                sh "docker build -t ${env.DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Use the Jenkins credentials configured with ID 'docker-hub-credentials'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                    echo "--- Logging in and pushing to Docker Hub..."
                    
                    // 1. Log in to Docker Hub
                    sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}"
                    
                    // 2. Push the image
                    sh "docker push ${env.DOCKER_IMAGE}:latest"
                    
                    // 3. Log out for security
                    sh "docker logout"
                }
            }
        }
    }
}