// Jenkinsfile
pipeline {
    agent any

    environment {
        // !! UPDATE THIS: Replace with your actual Docker Hub username and Roll Number !!
        DOCKER_IMAGE = "imt2023091/ci-cd-demo"
        // Ensure this ID matches the ID set in Jenkins Credentials
        DOCKER_CREDS_ID = "docker-hub-creds" 
    }

    stages {
        stage('Login & Setup') {
            steps {
                echo "--- Logging in to Docker Hub for rate limit protection..."
                // Perform a secure login that lasts for the rest of the node's execution
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                    sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASSWORD}"
                }
            }
        }
        
        stage('Test (Pytest in Docker)') {
            steps {
                script {
                    echo "--- Running automated Pytest tests inside a Docker container..."
                    
                    // This command will now execute as an authenticated user, avoiding the rate limit error!
                    sh '''
                        docker run --rm \
                        -v "${PWD}":/app \
                        -w /app \
                        python:3.10-slim /bin/bash -c "pip install -r requirements.txt && python -m pytest test_todo.py"
                    '''
                    
                    echo "Tests passed successfully in isolated Docker environment!"
                }
            }
        }

        stage('Create Docker Image') {
            steps {
                echo "--- Building final Docker image: ${env.DOCKER_IMAGE}:latest"
                sh "docker build -t ${env.DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "--- Pushing to Docker Hub..."
                // The image is already tagged with the full name, no need to retag.
                // The login is already active from the 'Login & Setup' stage.
                sh "docker push ${env.DOCKER_IMAGE}:latest"
            }
        }
    }
    
    post {
        // Always try to log out, even if the pipeline fails
        always {
            echo "--- Ensuring Docker Hub logout for security..."
            // It's safe to use a separate 'sh docker logout' if the original login succeeded
            sh 'docker logout || true' // '|| true' ensures the pipeline doesn't fail on logout if it was never logged in
        }
    }
}