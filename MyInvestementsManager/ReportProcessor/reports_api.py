from MyInvestementsManager.ReportProcessor.reports_extractor import extract_annual_report_data
from MyInvestementsManager.ReportProcessor.reports_store import store_report_tables
from MyInvestementsManager.models import ListedCompany


# def process_tables_from_annual_reports():
#      print("Process annual reports")
#      all_companies = ListedCompany.objects.all()
#      for company in all_companies:
#          print(company.symbol)
#          tables_in_reports = extract_annual_report_data(company.symbol)
#          print("Number of reports = " + str(len(tables_in_reports)))
#          for tables_in_one_report in tables_in_reports:
#              store_report_tables(company, tables_in_one_report['date'], tables_in_one_report['name'],
#                                  tables_in_one_report['tables'])


def process_tables_from_annual_reports():
    company = ListedCompany.objects.first()
    date = 1558636200000
    name = "test report"
    tables = "test tables"

    store_report_tables(company, date, name,
                                     tables)






