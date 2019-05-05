from MyInvestementsManager.ReportProcessor.reports_extractor import extract_annual_report_data
from MyInvestementsManager.models import ListedCompany


def get_annual_report_data():
    return None


def process_annual_report_data():
    print("Process annual reports")
    all_companies = ListedCompany.objects.all()
    for company in all_companies:
        extract_annual_report_data(company.symbol)



