#!/bin/bash

# just for testing

set -e

BUILDPLATFORM=linux/arm64/v8

(
    DOCKER_BUILDKIT=1 docker build . --no-cache --target production \
      --build-arg REPOSITORY_SITE_ORGANIZATION='' \
      --build-arg REPOSITORY_SITE_NAME='nr-docs' \
      --build-arg REPOSITORY_IMAGE_URL='' \
      --build-arg REPOSITORY_AUTHOR='ms <ms@ms.com>' \
      --build-arg REPOSITORY_GITHUB_URL='' \
      --build-arg REPOSITORY_URL='https://docs.narodni-repozitar.cz' \
      --build-arg REPOSITORY_DOCUMENTATION='https://docs.narodni-repozitar.czdocumentation' \
      --build-arg BUILDPLATFORM=$BUILDPLATFORM \
      -t cesnet/mytest:11 \
      -t cesnet/mytest:latest -f ./sites/mysite/docker/Dockerfile.production
)