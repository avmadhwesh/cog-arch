#!/usr/bin/env bash

jspsychUrl="https://github.com/jspsych/jsPsych/releases/download/v6.1.0/jspsych-6.1.0.zip"

curl -L "$jspsychUrl" > jspsych-6.1.0.zip
checksum="$(sha256sum jspsych-6.1.0.zip | cut -d ' ' -f 1)"

if [[ ! "$checksum" = "7fe966fec089b8f2feeee0404187106edf42db768a7e2d84985ed738f4a3a850" ]]
then
  echo "Checksum did not match!" > /dev/stderr
  exit 1
fi

unzip jspsych-6.1.0.zip -d jspsych-6.1.0
rm jspsych-6.1.0/examples -rf
rm jspsych-6.1.0.zip
