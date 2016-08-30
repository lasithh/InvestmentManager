from django.contrib import admin
from MyInvestementsManager.models import Investment, ListedCompany,\
    DailyTradeSummary, CompanyIssuedQuantitiesHistory, DetailedTrade


admin.site.register(Investment)
admin.site.register(ListedCompany)
admin.site.register(DailyTradeSummary)
admin.site.register(CompanyIssuedQuantitiesHistory)
admin.site.register(DetailedTrade)
# Register your models here.
