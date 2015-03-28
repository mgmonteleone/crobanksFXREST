#!/bin/sh
docker stop crofxrest
docker rm crofxrest
docker run -d -p 5006:5000 -e mydockerhost=`hostname -f` --restart=on-failure:10 --name crofxrest dkrs.co/crofxrest
