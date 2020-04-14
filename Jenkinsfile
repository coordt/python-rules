pipeline {
    agent {
        docker {
            image 'python:3.7'
        }
    }

    environment {
        PYTHONUSERBASE = "${env.WORKSPACE}"
        PATH = "${env.WORKSPACE}/bin:${env.PATH}"
    }

    stages {
        stage("Code pull") {
            steps {
                checkout scm
            }
        }

        stage('Build environment') {
            steps {
                sh "PATH=$WORKSPACE/bin:$PATH pip install --user --no-cache-dir -r requirements/dev.txt"
            }
        }

        stage('Run tox Environments') {
            steps {
                script {
                    def envs = sh(returnStdout: true, script: "PATH=$WORKSPACE/bin:$PATH tox -l").trim().split('\n')
                    def cmds = envs.collectEntries({ tox_env ->
                        [tox_env, {
                            sh "PATH=$WORKSPACE/bin:$PATH tox --parallel--safe-build -vve $tox_env"
                        }]
                    })
                    parallel(cmds)
                }
                recordIssues(tools: [flake8(pattern: 'flake8-errors.txt')])
            }
            post{
                always{
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: true, keepAll: false, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'Coverage Line Report', reportTitles: ''])
                    step([$class: 'CoberturaPublisher',
                             autoUpdateHealth: true,
                             autoUpdateStability: true,
                             coberturaReportFile: 'coverage.xml',
                             failNoReports: false,
                             failUnhealthy: false,
                             failUnstable: false,
                             maxNumberOfBuilds: 10,
                             onlyStable: false,
                             sourceEncoding: 'ASCII',
                             zoomCoverageChart: false])
                }
            }
        }

        stage("PyPi") {
            when {
                buildingTag()
            }
            environment {
                PYPI_URL = "http://lin2pr1gp1n6:8080/"
                PYPI = credentials('PyPi')
            }
            steps {
                sh '''python setup.py bdist_wheel
                      twine upload dist/*  --verbose --repository-url ${PYPI_URL} -u ${PYPI_USR} -p ${PYPI_PSW}
                   '''
            }
            post {
                always {
                    archiveArtifacts(allowEmptyArchive: true, artifacts: 'dist/*whl', fingerprint: true)
                }
            }
        }
    }

    post {
        always{`
            sh "make clean"
        }
        failure {
            emailext(subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                     body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                     <p>Check console output at <a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a></p>""",
                     attachLog: true,
                     compressLog: true,
                     mimeType: 'text/html',
                     recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
    }

    options {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
}
