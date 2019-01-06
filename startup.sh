#!/bin/bash
cd /home/computer/workspace/MyProject1

#Pulls latest changes
git pull

#Start the service
python manage.py runserver 0.0.0.0:8000 > output

