// The following block for build , test code 
// pipeline {
//     agent any

//     environment {
//         IMAGE_NAME = "woodzone-website"
//         CONTAINER_NAME = "woodzone-website"
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 git 'https://github.com/jafar90147677/WoodZone2-website.github.io.git'
//             }
//         }

//         stage('Run Selenium Tests') {
//             steps {
//                 sh '''
//                     # Setup Python virtual env
//                     python3 -m venv venv
//                     . venv/bin/activate

//                     pip install --upgrade pip
//                     pip install pytest selenium

//                     # Start simple HTTP server in background
//                     python3 -m http.server 8000 &
//                     SERVER_PID=$!

//                     # Run Selenium tests
//                     pytest -v test_homepage.py || EXIT_CODE=$?

//                     # Kill server after tests
//                     kill $SERVER_PID || true

//                     # Exit if pytest failed
//                     if [ ! -z "$EXIT_CODE" ]; then
//                         exit $EXIT_CODE
//                     fi
//                 '''
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 sh '''
//                     docker build -t $IMAGE_NAME .
//                 '''
//             }
//         }

//         stage('Deploy Docker Container') {
//             steps {
//                 sh '''
//                     # Stop old container if running
//                     docker stop $CONTAINER_NAME || true
//                     docker rm $CONTAINER_NAME || true

//                     # Run new container
//                     docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME
//                 '''
//             }
//         }
//     }
// }





pipeline {
    agent any

    stages {
        stage('Build & Test') {
            steps {
                sh '''
                  python3 -m venv venv
                  . venv/bin/activate
                  pip install -r requirements.txt
                  pytest -v test_homepage.py
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t woodzone-website:latest .'
            }
        }

        stage('Deploy to Docker') {
            steps {
                sh '''
                  docker rm -f woodzone-website || true
                  docker run -d -p 8000:8000 --name woodzone-website woodzone-website:latest
                '''
            }
        }
    }
}
