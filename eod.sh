#!/usr/bin/expect

#Pull remote repository
git pull

#Download latest data
echo "loading eod data"
curl -v http://127.0.0.1:8000/loadLatestData

echo "Load financial Tables"
curl -v http://127.0.0.1:8000/extractFinancialReports

#Git commit and push
git add -A

#Commit
git commit -a -m "Daily Update"
git push
