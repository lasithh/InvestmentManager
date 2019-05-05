from django.conf.urls import url
from . import views
from MyInvestementsManager.views import InvestmentsListView, \
    InvestmentDetailView, InvestmentDeleteView, \
    InvestmentUpdateView, ListedCompanyView, ListedCompanyListView, \
    DailyTradingSummaryListView, DailyTradingSummaryView, DetailedTradeListView, \
    DetailedTradeView, SectorIndexListView, SectorIndexView, \
    InvestmentCreateView, DividendsCreateView, \
    CompanyFinanceReportSumaryListView, CompanyFinanceReportSumaryCreateView, \
    CompaniesWithFinanceReportSumaryListView, DividendListView

urlpatterns = [
    url(r'^invest$', views.index, name='index'),
    # investmets related urls
    url(r'^investmetsList$', InvestmentsListView.as_view()),
    url(r'^addInvestment$', InvestmentCreateView.as_view(), name='add_investment'),
    url(r'^viewInvestment/(?P<pk>\d+)/$', InvestmentDetailView.as_view(), name='view_investment'),
    url(r'^deleteInvestment/(?P<pk>\d+)/$', InvestmentDeleteView.as_view(), name='delete_investment'),
    url(r'^updateInvestment/(?P<pk>\d+)/$', InvestmentUpdateView.as_view(), name='update_investment'),

    # Symbols related urls
    url(r'^reloadCompaniesList$', views.updateSymbolsList, name='updateSymbolsList'),
    url(r'^companiesList$', ListedCompanyListView.as_view()),
    url(r'^viewCompany/(?P<pk>\d+)/$', ListedCompanyView.as_view(), name='view_company'),

    # Trading summary related urls
    url(r'^dailyTradingSummaryList$', DailyTradingSummaryListView.as_view()),
    url(r'^viewTradingSummary/(?P<pk>\d+)/$', DailyTradingSummaryView.as_view(), name='view_trading_summary'),
    url(r'^storeDailyTradingSummary$', views.storeDailyTradingSummary, name='storeDailyTradingSummary'),

    # Detailed trades related urls
    url(r'^detailedTradesList$', DetailedTradeListView.as_view()),
    url(r'^viewDetailedTrade/(?P<pk>\d+)/$', DetailedTradeView.as_view(), name='view_detailed_trade'),
    url(r'^storeDetailedTrades$', views.storeDetailedTrades, name='storeDetailedTrades'),

    # Sector Indices related urls
    url(r'^sectorIndicesList$', SectorIndexListView.as_view()),
    url(r'^viewSectorIndex/(?P<pk>\d+)/$', SectorIndexView.as_view(), name='view_sector_index'),
    url(r'^storeSectorIndices$', views.storeSectorIndices, name='storeSectorIndices'),

    # Load latest data from the exchange
    url(r'^loadLatestData$', views.loadLatestData, name='loadLatestData'),

    # Dividends
    url(r'^addDividend/(?P<investmentId>[0-9]+)/$', DividendsCreateView.as_view(), name='add_dividend'),
    url(r'^loadDividends$', DividendListView.as_view()),

    # Finacial Data
    url(r'^financialDataList$', CompaniesWithFinanceReportSumaryListView.as_view(),
        name='companies_with_finance_report_summary'),
    url(r'^addCompanyFinancialData$', CompanyFinanceReportSumaryCreateView.as_view(), name='add_financial_data'),
    url(r'^getCompanyFinancialHistory/$', CompanyFinanceReportSumaryListView.as_view(),
        name='company_finance_report_summary'),

    # Financial Reports
    url(r'^extractFinancialReports', views.extractFinancialReports, name='extractFinancialReports'),

]
