#!/bin/bash

set -e

docker compose pull

# docker ps -a | grep dairoot | awk '{print $1}' | xargs docker rm -f

docker compose up -d --remove-orphans

docker images |grep dairoot|grep none |awk '{print $3}' | xargs docker rmi > /dev/null 2>&1
