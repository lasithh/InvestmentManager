from django.contrib import admin
from MyInvestementsManager.models import Investment, ListedCompany, \
    DailyTradeSummary, CompanyIssuedQuantitiesHistory, DetailedTrade, \
    InvestmentType, Currency, CompanyFinanceReportSumary, SectorIndexNames, \
    SectorIndex, Dividend, DividendType, ReportTables

admin.site.register(Currency)
admin.site.register(InvestmentType)
admin.site.register(Investment)
admin.site.register(ListedCompany)
admin.site.register(DailyTradeSummary)
admin.site.register(CompanyIssuedQuantitiesHistory)
admin.site.register(DetailedTrade)
admin.site.register(CompanyFinanceReportSumary)
admin.site.register(SectorIndexNames)
admin.site.register(SectorIndex)
admin.site.register(Dividend)
admin.site.register(DividendType)
admin.site.register(ReportTables)

# Register your models here.
