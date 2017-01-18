#!/usr/bin/env groovy

node {
   	stage 'Start'
	   	echo 'Starting build for data-loader-api'
   	stage 'Checkout'
	   	git url: 'https://github.com/datastructr/data-loader-api.git', branch: 'master'
	stage 'Build'
		echo 'create virtualenv'
		sh 'pyvenv venv'
		echo 'activate venv'
		sh 'source venv/bin/activate'
		echo 'install packages'
		sh 'pip install -r requirements.txt'
		sh "ls -la ${pwd()}"
		echo 'running tests'
		sh 'python setup.py test'
	stage 'Publish'
		publishHTML (target: [
			allowMissing: false,
			alwaysLinkToLastBuild: false,
			keepAll: true,
			reportDir: 'htmlcov',
			reportFiles: 'index.html',
			reportName: "Data Loader API"
		])
}
