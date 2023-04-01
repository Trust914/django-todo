pipeline {
  agent any
  tools {
//    maven "Maven3"
    jdk "OracleJDK"
  }

  environment {
    registryCredential = 'REGISTRY_CREDENTIALS'
    appRegistry = "AWS_ECR_REGISTRY"
    vprofileRegistry = "AWS_ECR_REGISTRY_URL"
    cluster = "YOUR_DJANGO_CLUSTER_ON_AWS"
    service = "YOUR_DJANGO_SERVICE_ON_AWS"
  }
  stages {
    stage('Fetch code'){
      steps {
        //git branch: 'main', url: 'https://github.com/Trust914/django-todo.git'
	 checkout([$class: 'GitSCM',
                branches: [[name: '*/main' ]],
                extensions: scm.extensions,
                userRemoteConfigs: [[
                    url: 'git@github.com:Trust914/django-todo.git',
                    credentialsId: 'GITHUB_CREDENTIALS'
                ]]
            ])
      }
    }

    stage('build && SonarQube analysis') {
      environment {
       scannerHome = tool 'Sonar4'
      }
      steps {
          withSonarQubeEnv('Sonar') {
           sh '''${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=django-todo \
             -Dsonar.projectName=django-todo-project \
             -Dsonar.projectVersion=1.0 \
             -Dsonar.sources=. \
             
             '''
          }
      }
    }
    stage("Quality Gate") {
        steps {
          timeout(time: 1, unit: 'HOURS') {
            // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
            // true = set pipeline to UNSTABLE, false = don't
            waitForQualityGate abortPipeline: true
          }
        }
      }
    stage('Build App Image') {
     steps {
     
       script {
          dockerImage = docker.build( appRegistry + ":$BUILD_NUMBER", "./")
        }
      }
    }

    stage('Upload App Image') {
      steps{
        script {
          docker.withRegistry( vprofileRegistry, registryCredential ) {
            dockerImage.push("$BUILD_NUMBER")
            dockerImage.push('latest')
          }
        }
      }
    }
    stage('Deploy image on ECS') {
      steps {
        withAWS(credentials: 'awscreds', region: 'us-east-1') {
          sh "aws ecs update-service --cluster ${cluster} --service ${service} --force-new-deployment"
        }
      }
    }
  }
}
