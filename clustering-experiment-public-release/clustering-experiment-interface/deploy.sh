#!/usr/bin/env bash

npx webpack -p
ssh server << EOF
  mkdir /websites/experiments.vijaymarupudi.com/clustering -p
EOF
rsync dist/ server:/websites/experiments.vijaymarupudi.com/clustering -aP
