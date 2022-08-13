#!/usr/bin/env bash

echo "Running After Install Scripts..."
sudo apt install libpython3.9-dev
sudo pip3 install django-rest-swagger
sudo pip install pymongo
sudo pip install pymongo[srv]
sudo mkdir /var/www/backend/src/static_root/
sudo mkdir /var/www/backend/static_root/
sudo python3 /var/www/backend/src/manage.py collectstatic
echo "Collected Static Files"
