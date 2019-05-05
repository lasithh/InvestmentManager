import json
import os
import urllib2

from MyInvestementsManager.ReportProcessor.pdf_reader import extract_tables
from MyInvestementsManager.util.ApplicationConstants import URL_CSE, URL_CDN
from MyInvestementsManager.util.HTTPModule.HttpInterface import getDataByHttpsWithBody, download_file


def extract_annual_report_data(symbol):
    urls = extract_annual_report_urls(symbol)
    print(symbol)
    for url in urls:
        complete_url = URL_CDN + "/" + url[1]

        print(complete_url)

        download_file(complete_url, "temp_file.pdf")
        tables = extract_tables("temp_file.pdf")

        total_tables = sum(len(v) for v in tables.itervalues())

        print("number of tables: " + str(total_tables))

def extract_annual_report_urls(symbol):
    paths = list()
    params = {'symbol': str(symbol)}
    all_reports = getDataByHttpsWithBody('https://' + URL_CSE + '/api/financials', params)
    json_data = json.loads(all_reports)
    for report in json_data['infoAnnualData']:
        if 'Annual Report' in report['fileText']:
            path = report['path']
            name = report['fileText']
            paths.append(tuple((name, path)))
    return paths

def delete_file(file_path):
    os.remove(file_path)
