// Define environment variables
environment {
    // Based on console output, IMT2023091 is the Docker Hub username
    DOCKER_HUB_USER = 'IMT2023091'
    IMAGE_NAME = "ci-cd-demo"
    // Generates a unique tag based on the Jenkins build number
    IMAGE_TAG = "${env.BUILD_NUMBER}" 
    // Credential ID matching the one configured in Jenkins (Username/Token)
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
            // Using python3 command as 'python' was not found on the Jenkins host
            sh 'python3 test_todo.py'
            sh 'echo "Tests passed successfully."'
        }
    }

    // Combined Build and Push stage. Docker login must happen BEFORE the build 
    // to authenticate the pull of the base image (python:3.10-slim), resolving the 429 error.
    stage('Build and Push Image') {
        steps {
            script {
                def fullImageName = "${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"

                // 1. Securely log in to Docker Hub using stored credentials
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    
                    echo "Logging into Docker Hub for pull and push..."
                    // Log in using the Docker Hub Access Token as the password
                    sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                    
                    // 2. Build the Docker Image
                    echo "Building Docker image: ${fullImageName}"
                    sh "docker build -t ${fullImageName} ."
                    
                    // 3. Push to Docker Hub
                    echo "Pushing image tag ${IMAGE_TAG} to Docker Hub..."
                    sh "docker push ${fullImageName}"
                    
                    echo "Tagging and pushing 'latest'..."
                    sh "docker tag ${fullImageName} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                    
                    echo "Image pushed successfully to Docker Hub."
                    
                    // 4. Logout for security
                    sh "docker logout"
                }
            }
        }
    }
    
    stage('Deploy Container') {
        steps {
            script {
                // Deploy stage pulls the newly pushed image from Docker Hub
                def latestImage = "${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                echo "Deploying container by pulling from Docker Hub..."
                sh """
                    # Stop and remove the old container instance (|| true prevents script failure if container doesn't exist)
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    # Run the new container, pulling the 'latest' image from the registry
                    docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${latestImage}
                    echo "Container ${CONTAINER_NAME} deployed and running on port 5000."
                """
            }
        }
    }
}
// Jenkinsfile
// Revised Pipeline: Wrapped in a 'script' block to bypass persistent 'stages' method error.

script {
    pipeline {
        agent any

        // Define environment variables
        environment {
            // Based on console output, IMT2023091 is the Docker Hub username
            DOCKER_HUB_USER = 'IMT2023091'
            IMAGE_NAME = "ci-cd-demo"
            // Generates a unique tag based on the Jenkins build number
            IMAGE_TAG = "${env.BUILD_NUMBER}" 
            // Credential ID matching the one configured in Jenkins
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
                    // Using python3 now that we know 'python' failed
                    sh 'python3 test_todo.py'
                    sh 'echo "Tests passed successfully."'
                }
            }

            // Combined Build and Push stage. Login before build fixes the 429 rate limit error.
            stage('Build and Push Image') {
                steps {
                    script {
                        def fullImageName = "${DOCKER_HUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"

                        // 1. Securely log in to Docker Hub using stored credentials
                        withCredentials([usernamePassword(credentialsId: DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            
                            echo "Logging into Docker Hub for pull and push..."
                            // Log in using the Docker Hub Access Token as the password
                            sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                            
                            // 2. Build the Docker Image
                            echo "Building Docker image: ${fullImageName}"
                            sh "docker build -t ${fullImageName} ."
                            
                            // 3. Push to Docker Hub
                            echo "Pushing image tag ${IMAGE_TAG} to Docker Hub..."
                            sh "docker push ${fullImageName}"
                            
                            echo "Tagging and pushing 'latest'..."
                            sh "docker tag ${fullImageName} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                            sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                            
                            echo "Image pushed successfully to Docker Hub."
                            
                            // 4. Logout for security
                            sh "docker logout"
                        }
                    }
                }
            }
            
            stage('Deploy Container') {
                steps {
                    script {
                        // Deploy stage pulls the newly pushed image from Docker Hub
                        def latestImage = "${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                        echo "Deploying container by pulling from Docker Hub..."
                        sh """
                            # Stop and remove the old container instance
                            docker stop ${CONTAINER_NAME} || true
                            docker rm ${CONTAINER_NAME} || true
                            # Run the new container
                            docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${latestImage}
                            echo "Container ${CONTAINER_NAME} deployed and running on port 5000."
                        """
                    }
                }
            }
        }
    }
}