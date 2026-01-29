pipeline {
    agent any
    
    environment {
        // Python environment
        PYTHONUNBUFFERED = '1'
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code from GitHub...'
                checkout scm
                sh 'ls -la'
                sh 'pwd'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    python3 --version
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip
                    pip --version
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo '📚 Installing Python dependencies...'
                sh '''
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }
        
        stage('Run API Tests') {
            steps {
                echo '🔌 Running Backend API Tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/backend/api/ -v \
                        --html=reports/api_report.html \
                        --self-contained-html \
                        --junit-xml=reports/api_results.xml \
                        || true
                '''
            }
        }
        
        stage('Run UI Tests') {
            steps {
                echo '🖥️ Running Frontend UI Tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/frontend/pw/ -v \
                        --html=reports/ui_report.html \
                        --self-contained-html \
                        --junit-xml=reports/ui_results.xml \
                        --screenshot=only-on-failure \
                        --video=retain-on-failure \
                        || true
                '''
            }
        }
        
        stage('Publish Reports') {
            steps {
                echo '📊 Publishing HTML reports...'
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'api_report.html, ui_report.html',
                    reportName: 'Test Reports',
                    reportTitles: 'API Tests, UI Tests'
                ])
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo '💾 Archiving test artifacts...'
                archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
                junit testResults: 'reports/*.xml', allowEmptyResults: true
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            cleanWs()
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
