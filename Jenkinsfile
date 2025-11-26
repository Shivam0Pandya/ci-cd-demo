// Jenkinsfile
// Optimized Declarative Pipeline for Local Docker Desktop CI/CD.
// This script assumes Jenkins and Docker Desktop are running on the same host
// and the Jenkins user has permission to run 'docker' commands.

pipeline {
    // Pipeline runs on any available Jenkins agent (your main host machine)
    agent any

    // Define environment variables for clean configuration
    environment {
        // Tag the image locally using the unique Jenkins BUILD_NUMBER
        IMAGE_NAME = "ci-cd-demo"
        IMAGE_TAG = "${env.BUILD_NUMBER}" 
        // Name for the running container instance
        CONTAINER_NAME = "ci-cd-demo-app"
    }

    stages {
        stage('Pull Code') {
            steps {
                // For a Pipeline job configured with SCM, the code is checked out automatically
                sh 'echo "Code successfully pulled from GitHub: https://github.com/Shivam0Pandya/ci-cd-demo.git"'
            }
        }

        stage('Test Code') {
            steps {
                // Execute the unit tests using Python's built-in unittest framework.
                // The pipeline will fail here if any tests in 'test_todo.py' fail.
                sh 'echo "Running unit tests..."'
                sh 'python test_todo.py'
                sh 'echo "Tests passed successfully."'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def fullImageName = "${IMAGE_NAME}:${IMAGE_TAG}"
                    echo "Starting Docker image build for tag: ${fullImageName}"
                    
                    // Build the Docker image using the Dockerfile in the current directory
                    sh "docker build -t ${fullImageName} ."
                    
                    echo "Docker image built successfully."
                }
            }
        }

        // The 'Push to Docker Hub' stage is omitted since we are deploying locally

        stage('Deploy Container') {
            steps {
                script {
                    def currentImage = "${IMAGE_NAME}:${IMAGE_TAG}"
                    echo "Starting local deployment to Docker Desktop..."
                    sh """
                        # 1. Stop and remove the old container instance (if it exists)
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        
                        # 2. Run the new container in detached mode (-d), mapping the exposed port 5000.
                        docker run -d -p 5000:5000 --name ${CONTAINER_NAME} ${currentImage}
                        
                        echo "Container ${CONTAINER_NAME} deployed and running on port 5000."
                    """
                }
            }
        }
    }
}