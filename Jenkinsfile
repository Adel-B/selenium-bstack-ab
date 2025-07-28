pipeline {
    agent any
    
    environment {
        // BrowserStack credentials (configure these in Jenkins)
        BROWSERSTACK_CREDS = credentials('browserstack-creds')
        EXECUTION_MODE = 'browserstack'
    }
    
    stages {
        stage('Setup') {
            steps {
                echo "🔄 Checking out code and setting up environment..."
                
                // Checkout code first
                checkout scm
                
                script {
                    if (isUnix()) {
                        sh '''
                            # Install uv if not present
                            if ! command -v uv &> /dev/null; then
                                curl -LsSf https://astral.sh/uv/install.sh | sh
                            fi
                            
                            # Add uv to PATH
                            export PATH="$HOME/.local/bin:$PATH"
                            
                            # Verify we have pyproject.toml
                            ls -la pyproject.toml
                            
                            # Install dependencies (including dev tools)
                            uv sync --extra dev
                            
                            # Create reports directory
                            mkdir -p test-reports
                        '''
                    } else {
                        bat '''
                            REM Install uv if not present
                            where uv >nul 2>nul || powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
                            
                            REM Add uv to PATH (Windows)
                            set PATH=%USERPROFILE%\\.cargo\\bin;%PATH%
                            
                            REM Verify we have pyproject.toml
                            dir pyproject.toml
                            
                            REM Install dependencies (including dev tools)
                            uv sync --extra dev
                            
                            REM Create reports directory
                            mkdir test-reports
                        '''
                    }
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                echo "🔍 Running code quality checks..."
                script {
                    if (isUnix()) {
                        sh '''
                            # Add uv to PATH
                            export PATH="$HOME/.local/bin:$PATH"
                            
                            echo "📝 Formatting code with Black..."
                            uv run black --check --diff .
                            
                            echo "🔍 Linting with Ruff..."
                            uv run ruff check .
                            
                            echo "🔎 Type checking with MyPy..."
                            uv run mypy .
                        '''
                    } else {
                        bat '''
                            REM Add uv to PATH (Windows)
                            set PATH=%USERPROFILE%\\.cargo\\bin;%PATH%
                            
                            echo 📝 Formatting code with Black...
                            uv run black --check --diff .
                            
                            echo 🔍 Linting with Ruff...
                            uv run ruff check .
                            
                            echo 🔎 Type checking with MyPy...
                            uv run mypy .
                        '''
                    }
                }
            }
        }
        
        stage('Run BrowserStack Tests') {
            steps {
                echo "☁️ Running Galaxy S20+ tests on 3 browsers..."
                script {
                    if (isUnix()) {
                        sh '''
                            # Add uv to PATH
                            export PATH="$HOME/.local/bin:$PATH"
                            
                            # Set BrowserStack credentials from Jenkins
                            export BROWSERSTACK_USERNAME="$BROWSERSTACK_CREDS_USR"
                            export BROWSERSTACK_ACCESS_KEY="$BROWSERSTACK_CREDS_PSW"
                            
                            echo "Username: $BROWSERSTACK_CREDS_USR***"
                            
                            # Run only BrowserStack tests (3 platforms)
                            echo "🚀 Running BrowserStack tests on 3 platforms..."
                            uv run browserstack-sdk pytest tests/test_samsung_favorite_galaxy.py::test_favorite_galaxy_browserstack \
                                -v \
                                --junit-xml=test-reports/results.xml \
                                --html=test-reports/report.html \
                                --self-contained-html
                        '''
                    } else {
                        bat '''
                            REM Add uv to PATH (Windows)
                            set PATH=%USERPROFILE%\\.cargo\\bin;%PATH%
                            
                            REM Set BrowserStack credentials from Jenkins
                            set BROWSERSTACK_USERNAME=%BROWSERSTACK_CREDS_USR%
                            set BROWSERSTACK_ACCESS_KEY=%BROWSERSTACK_CREDS_PSW%
                            
                            echo Username: %BROWSERSTACK_CREDS_USR%***
                            
                            REM Run only BrowserStack tests (3 platforms)
                            echo Running BrowserStack tests on 3 platforms...
                            uv run browserstack-sdk pytest tests/test_samsung_favorite_galaxy.py::test_favorite_galaxy_browserstack ^
                                -v ^
                                --junit-xml=test-reports/results.xml ^
                                --html=test-reports/report.html ^
                                --self-contained-html
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Publish test results using junit
            junit testResults: 'test-reports/results.xml', allowEmptyResults: true
            
            // Archive test artifacts (including HTML reports)
            archiveArtifacts artifacts: 'test-reports/**/*', allowEmptyArchive: true
            
            echo "📋 Test reports archived."
            echo "📊 Report: test-reports/report.html"
        }
        
        success {
            echo "✅ All 3 BrowserStack tests passed!"
        }
        
        failure {
            echo "❌ Some tests failed. Check the report for details."
        }
    }
} 