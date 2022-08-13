#!/usr/bin/env bash

echo "Stopping Zipcho Development App"
sudo supervisorctl stop all
sudo fuser -k 8000/tcp
echo "Stopped all Zipcho Services"

