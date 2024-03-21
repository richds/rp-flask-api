pipeline {
    agent { 
        dockerfile {
            additionalBuildArgs '--tag rpflask:jenkinstest'
            args ' -v $WORKSPACE:/results'
        }
    }
    environment {
        HOME = '${env.WORKSPACE}'
    }
    stages {
        stage('buildapp') {
            steps {
                sh 'python3 --version'
            }
        }
        stage('test'){
            steps {
                catchError (buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh 'python3 build_database.py'
                    sh 'python3 app.py &'
                    dir ("tests") {
                    sh 'pytest -svv api_test.py --junitxml=/results/test_results.xml'
                    }
                }
            }
        }
    }
    post {
        always {
            junit '**/test_results.xml'
        }
    }
}