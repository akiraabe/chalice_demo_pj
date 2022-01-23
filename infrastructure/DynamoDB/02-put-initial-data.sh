#!/bin/zsh

aws dynamodb batch-write-item --request-items file://initial-data.json