#!/usr/bin/expect

#Download latest data
#curl -v http://127.0.0.1:8000/loadLatestData

#Git commit and push
git add -A

#expect "login"
#Authenticate
#send "lasithh"
#cat << "gela1985@git"

#Commit
git commit -a -m "Daily Update"
git push
