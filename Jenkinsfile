// Pipeline de integración continua del módulo de pedidos.
// Jenkins lo ejecuta en cada rama del repositorio (Multibranch Pipeline):
// descarga el código, construye la imagen Docker, corre las pruebas dentro
// del contenedor, publica los resultados y, solo en main, marca la imagen
// como la última versión aprobada.

pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 15, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        IMAGEN = 'pedidos-ci'
    }

    stages {
        stage('1. Código') {
            steps {
                script {
                    env.TAG = sh(script: 'git rev-parse --short=7 HEAD', returnStdout: true).trim()
                    env.CONTENEDOR = "pedidos-e${env.EXECUTOR_NUMBER}-b${env.BUILD_NUMBER}"
                }
                echo "Rama: ${env.BRANCH_NAME} | Commit: ${env.TAG}"
                sh 'git log -1 --pretty=format:"%h %an %s"'
            }
        }

        stage('2. Construir imagen') {
            steps {
                sh 'docker version --format "Docker cliente {{.Client.Version}} / servidor {{.Server.Version}}"'
                sh 'docker build -t $IMAGEN:$TAG .'
            }
        }

        stage('3. Pruebas en contenedor') {
            steps {
                sh '''
                    mkdir -p reports
                    set +e
                    docker run --name "$CONTENEDOR" -e APP_ENV=pruebas "$IMAGEN:$TAG" \
                        pytest -v \
                        --junitxml=/app/reports/junit.xml \
                        --cov=pedidos --cov-report=term --cov-report=xml:/app/reports/coverage.xml
                    ESTADO=$?
                    set -e
                    docker cp "$CONTENEDOR:/app/reports/." reports/ || true
                    docker rm -f "$CONTENEDOR" > /dev/null
                    exit $ESTADO
                '''
            }
        }

        stage('4. Publicar imagen') {
            when { branch 'main' }
            steps {
                sh 'docker tag $IMAGEN:$TAG $IMAGEN:latest'
                echo "Imagen aprobada: ${env.IMAGEN}:${env.TAG} (también etiquetada como latest)"
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
            sh 'docker rm -f "$CONTENEDOR" > /dev/null 2>&1 || true'
        }
        success {
            echo 'Integración aprobada: todas las pruebas pasaron.'
        }
        failure {
            echo 'Integración rechazada: revisa las pruebas fallidas en "Test Result".'
        }
    }
}
