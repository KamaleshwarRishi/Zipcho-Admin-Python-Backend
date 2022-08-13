#!/usr/bin/env bash

sudo service nginx restart 
sudo supervisorctl start all
echo "Started All Zipcho Dev Services ....."