#!/usr/bin/env groovy

node {
   	stage 'Start'
	   	echo 'Starting build for data-loader-api'
   	stage 'Checkout'
	   	git url: 'https://github.com/datastructr/data-loader-api.git', branch: 'master'
	stage 'Build'
		echo 'create virtual env'
		sh 'pyvenv env'
		echo 'activate env'
		sh 'source env/bin/activate/
		echo 'install packages'
		sh 'pip install -r requirements.txt'
		sh "ls -la ${pwd()}"
		echo 'test'
		sh 'py.test'
}
