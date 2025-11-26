// Jenkinsfile
// Revised Declarative Pipeline for Docker Hub Integration (Standard CI/CD)

pipeline {
    agent any

    // Define environment variables
    environment {
        // !!! IMPORTANT: REPLACE 'YOUR_DOCKER_HUB_USER' with your actual Docker Hub username !!!
        DOCKER_HUB_USER = 'IMT2023091'
        IMAGE_NAME = "ci-cd-demo"
        // Generates a unique tag based on the Jenkins build number
        IMAGE_TAG = "${env.BUILD_NUMBER}" 
        // Credential ID matching the one configured in Jenkins (Username/Password for Docker Hub)
        DOCKER_CREDS_ID = 'docker-hub-creds'
        CONTAINER_NAME = "ci-cd-demo-app"
    }

    stages {
        stage('Pull Code') {
            steps {
                sh 'echo "Code successfully pulled from GitHub."'
            }
        }

        stage('Test Code') {
            steps {
                sh 'echo "Running unit tests..."'
                // Runs the tests using built-in unittest (from test_todo.py)
                sh 'python3 test_todo.py'
                sh 'echo "Tests passed successfully."'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Full tag includes the user name and version
                    def fullImageName = "${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    echo "Building Docker image: ${fullImageName}"
                    
                    // Build the Docker image using the Dockerfile
                    sh "docker build -t ${fullImageName} ."
                    
                    echo "Docker image built successfully."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    def fullImageName = "${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    
                    // Use 'withCredentials' to securely inject Docker Hub username and token
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        echo "Logging into Docker Hub..."
                        // Log in using the Docker Hub Access Token as the password
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                        
                        echo "Pushing image tag ${IMAGE_TAG} to Docker Hub..."
                        // Push the uniquely tagged image
                        sh "docker push ${fullImageName}"
                        
                        echo "Tagging and pushing 'latest'..."
                        // Tag and push 'latest' for easy reference
                        sh "docker tag ${fullImageName} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                        sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                        
                        echo "Image pushed successfully to Docker Hub."
                    }
                }
            }
        }
        
        stage('Deploy Container') {
            steps {
                script {
                    // Pull and run the 'latest' image we just pushed to the registry
                    def latestImage = "${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    echo "Deploying container by pulling from Docker Hub..."
                    sh """
                        # Pull the image we just pushed from the public registry
                        docker pull ${latestImage}
                        # Stop and remove the old container instance (|| true prevents script failure)
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        # Run the new container, mapping the port
                        docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${latestImage}
                        echo "Container ${CONTAINER_NAME} deployed and running on port 5000."
                    """
                }
            }
        }
    }
}