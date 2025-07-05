// Jenkinsfile
// Este script define o pipeline de CI/CD para o projeto Python.

pipeline {
    agent {
        docker {
            image 'docker:latest'

            args '-e DOCKER_HOST=tcp://host.docker.internal:2375 --user=0'
        }
    }

    // Opções globais para o pipeline
    options {
        // Define um tempo limite de 10 minutos para o pipeline, para evitar que ele fique preso.
        timeout(time: 10, unit: 'MINUTES')
        // Limpa o workspace antes de cada execução para garantir um ambiente limpo.
        skipDefaultCheckout()
    }

    // Declaração de variáveis de ambiente que serão usadas ao longo do pipeline.
    environment {
        BUILD_IMAGE = 'temperature-converter-python-build'
        TEST_IMAGE = 'temperature-converter-python-test'
        DOCKER_HOST = 'tcp://host.docker.internal:2375'
    }

    // Define as etapas (stages) do pipeline.
    stages {
        // Etapa de Checkout do Código Fonte
        stage('Checkout') {
            steps {
                script {
                    echo "Clonando o repositório GitHub..."
                    checkout scm
                }
            }
        }

        // Etapa de Construção das Imagens Docker
        stage('Build Docker Images') {
            steps {
                script {
                    echo "Construindo a imagem Docker para o build: ${BUILD_IMAGE}"
                    docker.build BUILD_IMAGE, '-f Dockerfile.build .'

                    echo "Construindo a imagem Docker para o teste: ${TEST_IMAGE}"
                    docker.build TEST_IMAGE, '-f Dockerfile.test .'
                }
            }
        }

        // Etapa de Execução dos Testes dentro de um Container Docker
        stage('Run Tests in Docker') {
          steps {
              script {
                  echo "Iniciando a execução dos testes dentro do container Docker..."

                  // VERSÃO CORRETA PARA O CENÁRIO 3
                  // Removemos o '-d' para que o Jenkins espere o resultado.
                  // Adicionamos o '--rm' para autolimpeza do contêiner.
                  // Usamos 'try/catch' para que a falha não pare a pipeline, mas a marque como instável.
                  try {
                      sh 'docker run --rm temperature-converter-python-test'
                  } catch (Exception e) {
                      // Marca o build atual como UNSTABLE
                      currentBuild.result = 'UNSTABLE'
                      // Opcional: imprime o erro no log
                      echo "Os testes falharam: ${e.getMessage()}"
                  }

                  echo "Execução dos testes concluída."
              }
          }
      }

    // Seções de Post-build (executadas após todas as stages)
    post {
        // Sempre executa, independentemente do resultado do pipeline.
        always {
            echo "Pipeline concluído."
            // Limpa as imagens Docker criadas para evitar acúmulo.
            script {
                try {
                    sh "docker rmi ${BUILD_IMAGE} ${TEST_IMAGE}"
                } catch (Exception e) {
                    echo "Erro ao remover imagens Docker: ${e.getMessage()}"
                }
            }
            // Limpa o workspace do Jenkins.
            cleanWs()
        }
        // Executa se o pipeline for bem-sucedido.
        success {
            echo 'Pipeline executado com SUCESSO!'
        }
        // Executa se o pipeline falhar.
        failure {
            echo 'Pipeline FALHOU!'
        }
        // Executa se o pipeline for instável (testes falharam, mas o build foi bem-sucedido).
        unstable {
            echo 'Pipeline INSTÁVEL (testes falharam)!'
        }
    }
}