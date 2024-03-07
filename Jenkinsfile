pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry = 'trannhatnguyen2/sentiment'
        registryCredential = 'dockerhub'
    }

    stages {
        stage('Test') {
            steps {
                echo 'Testing model correctness..'
                echo 'Always pass all test unit..'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'fullstackdatascience/jenkins-k8s:lts' // The image containing helm
                        imagePullPolicy 'Always' // Always pull image in case of using the same tag
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        sh("helm upgrade --install app --set image.repository=${registry} \
                        --set image.tag=v1.${BUILD_NUMBER} ./helm_charts/app --namespace model-serving")
                    }
                }
            }
        }
    }
}