properties([[$class: 'GitLabConnectionProperty', gitLabConnection: 'gitlab']])

pipeline {
  agent any

  options {
    disableConcurrentBuilds()
  }

  environment {
    TAG_NAME = "${(BRANCH_NAME + "_" + BUILD_ID).replaceAll("[.:/\\\\#]", '-')}"
    IMAGE_ID = "${IMAGE_NAME}:${TAG_NAME}"
    TAG_ALIAS = "${BRANCH_NAME == 'master' || BRANCH_NAME == 'release' ? BRANCH_NAME : 'latest'}"
  }

  stages {
    stage("run-tests") {
      steps {
        updateGitlabCommitStatus name: 'jenkins', state: 'running'
        sh 'make run_tests'
      }
    }

    stage('deploy-test') {
      environment {
        PROJECT_ROOT = '/srv/vdrive'
      }

      when {
        branch 'master'
      }

      steps {
        echo 'Starting deployment to test server (vdrive.atomcream.com)'
        script {
          sshagent(credentials: ['7c474019-b052-43ba-9b90-1a535d0e85dd']) {
            sh """
            expect -c '
                set timeout 300
                spawn ssh test-server
                expect "\\#"

                send "cd /srv/dusty_wall \\n"
                expect "\\#"

                send "git pull origin master \\n"
                expect "\\#"

                send "make docker_test_stop \\n"
                expect "\\#"

                send "make docker_test_up \\n"
                expect "\\#"

                send "docker logs --tail 1 -f vdrive_web_1 \\n"
                expect -re "*** uWSGI is running in multiple interpreter mode ***"

                send "exit \\n"
                expect eof
            '
            """
          }
        }
      }
    }
  }

  post {
    always {
      script {
        sh "docker run --rm -v `pwd`:/cmd mediasapiens/cmd /bin/bash -c 'cd /cmd/ && git clean -xfd'"
        sh "docker-compose -f docker-dev.yml down -v"
      }
      // cleans up workspace
      step([$class: 'WsCleanup'])
    }

    success {
        updateGitlabCommitStatus name: 'jenkins', state: 'success'
        slackSend "Success ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
    }

    failure {
        updateGitlabCommitStatus name: 'jenkins', state: 'failed'
        slackSend "Failed to build ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
    }

    unstable {
        updateGitlabCommitStatus name: 'jenkins', state: 'failed'
        slackSend "Failed to build ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
    }
  }

}

// will hit a specific url and make sure that it works as intended
def test_env() {
  // TODO: this needs to be more dynamic, we dont want to sit in this state
  // wait for dns / rancher to propagate
  wait_env_down();
  int interval = 1 //seconds
  int maxLoop = 120; // 2mins
  for (int i=0; i < maxLoop ; i++) {
    try{
        do_test_env();
        break;
    } catch(ex) {
        if (i == maxLoop - 1) {
            error(ex);
        } else {
            sleep(interval);
        }
     }
  }
}

def do_test_env() {
  String url = "https://${env.RANCHER_SUBDOMAIN_ALIAS}.${env.TARGET_DOMAIN}/v1/${env.RANCHER_STACK_NAME}/health"
  // TODO: add tests to make sure the upgrade succeeded on rancher
  // this stage should test just the rancher functionality (ie is it running still, can certain calls work)
  resp = sh( returnStdout: true, script: "curl -o /dev/null -w '%{http_code}' ${url}" ).trim()
  if( resp != '200' ) {
    error( "cant access ${url}" )
  }
}
