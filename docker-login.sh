#!/bin/sh

aws ecr get-login --no-include-email --profile dep --region us-east-1 | sh
