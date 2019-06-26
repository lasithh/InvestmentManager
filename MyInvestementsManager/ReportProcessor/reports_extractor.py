import datetime
import json
import os
import time

from MyInvestementsManager.ReportProcessor.pdf_reader import extract_tables
from MyInvestementsManager.ReportProcessor.reports_store import store_report_tables, is_report_exists
from MyInvestementsManager.util.ApplicationConstants import URL_CSE, URL_CDN
from MyInvestementsManager.util.HTTPModule.HttpInterface import getDataByHttpsWithBody, download_file


def extract_annual_report_data(company):
     metadata = extract_annual_report_metadata(company.symbol)
     all_tables = list()
     for metadata_one_report in metadata:
         print("Downloading report: " + metadata_one_report['name'])
         complete_url = URL_CDN + "/" + metadata_one_report['url']
         download_file(complete_url, "/tmp/temp_file.pdf")

         if not is_report_exists():
            tables = extract_tables("/tmp/temp_file.pdf")
            store_report_tables(company, metadata_one_report['date'], metadata_one_report['name'],tables)
         else:
             print("Report Exists. Company: " + company.symbol + "Name: " + metadata_one_report['name'])

         # Delete file
         os.remove("/tmp/temp_file.pdf")


     return all_tables


def extract_annual_report_metadata(symbol):
    return_data = list()
    params = {'symbol': str(symbol)}
    all_reports = getDataByHttpsWithBody('https://' + URL_CSE + '/api/financials', params)
    json_data = json.loads(all_reports)
    for report in json_data['infoAnnualData']:
        metadata = dict()
        if 'Annual Report' in report['fileText']:
            metadata['url'] = report['path']
            metadata['name'] = report['fileText']
            metadata['date'] = report['uploadedDate']
            return_data.append(metadata)
    return return_data

def delete_file(file_path):
    os.remove(file_path)
