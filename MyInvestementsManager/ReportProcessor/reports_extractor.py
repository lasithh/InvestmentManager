import json
import os

from MyInvestementsManager.ReportProcessor.pdf_reader import extract_tables
from MyInvestementsManager.util.ApplicationConstants import URL_CSE, URL_CDN
from MyInvestementsManager.util.HTTPModule.HttpInterface import getDataByHttpsWithBody, download_file


def extract_annual_report_data(symbol):
    print("Symbol: " + symbol)
    metadata = extract_annual_report_metadata(symbol)
    all_tables = list()
    for metadata_one_report in metadata:
        complete_url = URL_CDN + "/" + metadata_one_report['url']

        print("url : " + complete_url)

        download_file(complete_url, "temp_file.pdf")
        tables = extract_tables("temp_file.pdf")
        metadata_one_report['tables'] = tables
        all_tables.append(metadata_one_report)

    return all_tables


def extract_annual_report_metadata(symbol):
    return_data = list()
    params = {'symbol': str(symbol)}
    all_reports = getDataByHttpsWithBody('https://' + URL_CSE + '/api/financials', params)
    json_data = json.loads(all_reports)
    print(json_data)
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
