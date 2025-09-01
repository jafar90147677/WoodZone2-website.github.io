pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/jafar90147677/WoodZone2-website.github.io.git'
            }
        }
        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install pytest selenium
                '''
            }
        }
        stage('Run Server + Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -m http.server 8000 &
                    SERVER_PID=$!
                    sleep 3   # wait a bit for server
                    pytest -v test_homepage.py
                    kill $SERVER_PID
                '''
            }
        }
    }
}
