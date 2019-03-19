#!/bin/bash
cd /Users/hapu/myprojects/InvestmentAnalyser
#Pulls latest changes
git pull

#Start the service
nohup python manage.py runserver 0.0.0.0:8000 > output

