#!/bin/bash
cd /Users/hapu/myprojects/InvestmentAnalyser/MyProject1
#Pulls latest changes
git pull

#Start the service
python manage.py runserver 0.0.0.0:8000 > output

