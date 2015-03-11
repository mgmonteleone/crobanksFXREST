#!/bin/sh
docker stop croFxRest
docker rm croFxRest
docker run -d -p 5006:5000 -e mydockerhost=`hostname -f` --restart=on-failure:10 --name croFxRest dkrs.co/croFxRest
