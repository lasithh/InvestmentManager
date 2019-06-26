from MyInvestementsManager.ReportProcessor.reports_extractor import extract_annual_report_data
from MyInvestementsManager.ReportProcessor.reports_store import store_report_tables
from MyInvestementsManager.models import ListedCompany


def process_tables_from_annual_reports():
     print("Process annual reports")
     all_companies = ListedCompany.objects.all()
     for company in all_companies:
         print(company.symbol)
         tables_in_reports = extract_annual_report_data(company)






