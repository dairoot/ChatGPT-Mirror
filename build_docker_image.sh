#!/bin/bash

image=dairoot/chatgpt-mirror

# docker buildx build --platform linux/amd64 --push -t ${image} .
docker buildx build --platform linux/amd64,linux/arm64 --push -t ${image}:dev -t ${image}:0.1.0 -t ${image}:latest .
