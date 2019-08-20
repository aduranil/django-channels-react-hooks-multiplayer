pipeline {
    agent { docker { image 'python:3.7-stretch' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
