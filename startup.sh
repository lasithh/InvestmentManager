#!/bin/bash
cd /home/computer/myprojects/InvestmentManager
#Pulls latest changes
git pull

#Start the service
python manage.py runserver 0.0.0.0:8000 > output

