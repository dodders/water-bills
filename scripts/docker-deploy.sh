#!/bin/sh

scripts/docker-build.sh
scripts/docker-login.sh
scripts/docker-tag.sh
scripts/docker-push.sh
