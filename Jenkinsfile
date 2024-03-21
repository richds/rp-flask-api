pipeline {
    agent { dockerfile true }
    stages {
        stage('buildapp') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('test'){
            steps {
                catchError (buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh 'python3 app.py &'
                    dir ("tests") {
                    sh 'pytest -svx api_test.py'
                    }
                }
            }
        }
    }
}