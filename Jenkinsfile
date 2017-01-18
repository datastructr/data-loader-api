node {
   	stage 'Stage 1'
   		echo 'Starting build for data-loader-api'
   	stage 'Checkout'
   		git url: 'https://github.com/datastructr/data-loader-api.git'
   	stage 'Build'
   		sh './scripts/setup.sh'
   	stage 'Deploy'
   		sh './scripts/test.sh'
}
