#!/bin/bash
cd /home/pi/InvestmentManager
#Pulls latest changes
git pull

#Start the service
nohup python manage.py runserver 0.0.0.0:8000 > output 2>&1 &

