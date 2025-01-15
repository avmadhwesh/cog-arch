#!/bin/bash

trap 'kill $(jobs -p) && exit' INT # ^C handler, SIGTERMs all jobs and exits

# running these in bg using job control
cd serversrc
FLASK_ENV=development flask run &
cd ..
npx webpack-dev-server &

# don't exit the script until jobs are done
wait
