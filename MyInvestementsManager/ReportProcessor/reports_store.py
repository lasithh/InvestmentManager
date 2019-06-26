import datetime

from MyInvestementsManager.models import ReportTables


def store_report_tables(company, date, name, tables):
    ReportTables.objects.get_or_create(company=company,
                                       date = datetime.datetime.utcfromtimestamp(date / 1000.0),
                                       name = name,
                                       tables = tables
                                       )

def is_report_exists(company, date, name):
    return ReportTables.objects.filter(company=company, date = datetime.datetime.utcfromtimestamp(date / 1000.0),
                                name = name).exists()


