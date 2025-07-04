// Jenkinsfile
// Este script define o pipeline de CI/CD para o projeto Python.

// Define que o pipeline será executado em um agente Docker.
// Usamos a imagem 'docker:latest' que já vem com o cliente Docker CLI.
// Isso permite que o Jenkins execute comandos 'docker' diretamente dentro deste agente.
pipeline {
    agent {
        docker {
            image 'docker:latest' // Alterado para uma imagem que contém o Docker CLI
            // Monta o socket do Docker do host para que o agente possa interagir com o daemon Docker do host.
            // Isso é essencial para que o agente possa construir e gerenciar outros containers Docker.
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    // Opções globais para o pipeline
    options {
        // Define um tempo limite de 10 minutos para o pipeline, para evitar que ele fique preso.
        timeout(time: 10, unit: 'MINUTES')
        // Limpa o workspace antes de cada execução para garantir um ambiente limpo.
        // O checkout será feito manualmente para garantir que os Dockerfiles estejam presentes.
        skipDefaultCheckout()
    }

    // Declaração de variáveis de ambiente que serão usadas ao longo do pipeline.
    environment {
        // Define o nome da imagem Docker para o build.
        // O Jenkins irá construir esta imagem a partir do Dockerfile.build.
        BUILD_IMAGE = 'temperature-converter-python-build'
        // Define o nome da imagem Docker para os testes.
        // O Jenkins irá construir esta imagem a partir do Dockerfile.test.
        TEST_IMAGE = 'temperature-converter-python-test'
    }

    // Define as etapas (stages) do pipeline.
    stages {
        // Etapa de Checkout do Código Fonte
        stage('Checkout') {
            steps {
                script {
                    echo "Clonando o repositório GitHub..."
                    // Clona o repositório GitHub para o workspace do Jenkins.
                    // O 'scm' refere-se à configuração de SCM (Source Code Management) definida no job do Jenkins.
                    checkout scm
                }
            }
        }

        // Etapa de Construção das Imagens Docker
        stage('Build Docker Images') {
            steps {
                script {
                    echo "Construindo a imagem Docker para o build: ${BUILD_IMAGE}"
                    // Constrói a imagem Docker para o build usando o Dockerfile.build.
                    // O '.' indica que o Dockerfile está no diretório atual (workspace do Jenkins).
                    docker.build BUILD_IMAGE, '-f Dockerfile.build .'

                    echo "Construindo a imagem Docker para o teste: ${TEST_IMAGE}"
                    // Constrói a imagem Docker para o teste usando o Dockerfile.test.
                    docker.build TEST_IMAGE, '-f Dockerfile.test .'
                }
            }
        }

        // Etapa de Instalação de Dependências (equivalente ao "Build" em Python)
        stage('Install Dependencies in Docker') {
            steps {
                script {
                    echo "Iniciando a instalação de dependências Python dentro do container Docker..."
                    // Executa o comando 'pip install' dentro de um container da imagem BUILD_IMAGE.
                    // -v ${pwd()}:/app: Monta o diretório atual do workspace do Jenkins no /app dentro do container.
                    // Isso permite que o container acesse o código fonte e o requirements.txt.
                    docker.image(BUILD_IMAGE).inside("-v ${pwd()}:/app") {
                        sh 'pip install -r requirements.txt'
                    }
                    echo "Instalação de dependências Python concluída."
                }
            }
        }

        // Etapa de Execução dos Testes dentro de um Container Docker
        stage('Run Tests in Docker') {
            steps {
                script {
                    echo "Iniciando a execução dos testes dentro do container Docker..."
                    // Executa o comando 'pytest' dentro de um container da imagem TEST_IMAGE.
                    // Novamente, monta o workspace para que o container possa acessar o código e os testes.
                    docker.image(TEST_IMAGE).inside("-v ${pwd()}:/app") {
                        sh 'pytest tests/' // Executa os testes na pasta 'tests/'
                    }
                    echo "Execução dos testes concluída."
                }
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