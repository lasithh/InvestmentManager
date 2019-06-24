import datetime

from MyInvestementsManager.models import ReportTables


def store_report_tables(company, date, name, tables):
    print ("Storing: company " + company.symbol + " name: " + name + "date: " + str(date)   )
    ReportTables.objects.get_or_create(company=company,
                                       date = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H'),
                                       name = name,
                                       tables = tables
                                       )


