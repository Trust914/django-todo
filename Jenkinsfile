pipeline {
  agent any
  tools {
//    maven "Maven3"
    jdk "OracleJDK"
  }

  environment {
    registryCredential = 'ecr:us-east-1:awscreds'
    appRegistry = "869704209971.dkr.ecr.us-east-1.amazonaws.com/django-todo"
    vprofileRegistry = "https://869704209971.dkr.ecr.us-east-1.amazonaws.com"
    cluster = "django-todo-cluster"
    service = "django-todo-svc"
  }
  stages {
    stage('Fetch code'){
      steps {
        git branch: 'main', url: 'https://github.com/tushargangurde2029/django-todo.git'
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
