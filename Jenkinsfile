#!/usr/bin/env groovy

node {
   	stage 'Start'
	   	echo 'Starting build for data-loader-api'
   	stage 'Checkout'
	   	git url: 'https://github.com/datastructr/data-loader-api.git', branch: 'master'
	stage 'Build'
		sh './scripts/build.sh'
}