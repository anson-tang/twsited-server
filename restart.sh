#!/bin/bash

cd `dirname "$0"`

./stop_real.sh
echo "sleep 1 second ..."
sleep 1
./start.sh
