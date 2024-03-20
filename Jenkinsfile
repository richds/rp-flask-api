pipeline {
    agent {
        docker { image 'node:lts-alpine3.19' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'node --version'
            }
        }
    }
}