#!/bin/bash

image=dairoot/chatgpt-mirror:dev

# docker buildx build --platform linux/amd64 --push -t ${image} .
docker buildx build --platform linux/amd64,linux/arm64 --push -t ${image} .
