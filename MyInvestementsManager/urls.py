from django.conf.urls import url
from . import views
from MyInvestementsManager.views import InvestmentsListView,\
    InvestmentCreateView, InvestmentDetailView, InvestmentDeleteView,\
    InvestmentUpdateView,  ListedCompanyView, ListedCompanyListView,\
    DailyTradingSummaryListView, DailyTradingSummaryView, DetailedTradeListView,\
    DetailedTradeView


urlpatterns = [ 
    url(r'^invest$', views.index, name='index'),
               #investmets related urls   
    url(r'^investmetsList$', InvestmentsListView.as_view()),
    url(r'^addInvestment$', InvestmentCreateView.as_view(), name='add_investment'),     
    url(r'^viewInvestment/(?P<pk>\d+)/$', InvestmentDetailView.as_view(), name='view_investment'),
    url(r'^deleteInvestment/(?P<pk>\d+)/$', InvestmentDeleteView.as_view(), name='delete_investment'),
    url(r'^updateInvestment/(?P<pk>\d+)/$', InvestmentUpdateView.as_view(), name='update_investment'),
    
    #Symbols related urls
    url(r'^reloadCompaniesList$', views.updateSymbolsList, name='updateSymbolsList'),
    url(r'^companiesList$', ListedCompanyListView.as_view()),     
    url(r'^viewCompany/(?P<pk>\d+)/$', ListedCompanyView.as_view(), name='view_company'),
    
    #Trading summary related urls
    url(r'^dailyTradingSummaryList$', DailyTradingSummaryListView.as_view()),     
    url(r'^viewTradingSummary/(?P<pk>\d+)/$', DailyTradingSummaryView.as_view(), name='view_trading_summary'),
    url(r'^storeDailyTradingSummary$', views.storeDailyTradingSummary, name='storeDailyTradingSummary'),
    
    #Detailed trades related urls
    url(r'^detailedTradesList$', DetailedTradeListView.as_view()),     
    url(r'^viewDetailedTrade/(?P<pk>\d+)/$', DetailedTradeView.as_view(), name='view_detailed_trade'),
    url(r'^storeDetailedTrades$', views.storeDetailedTrades, name='storeDetailedTrades'),
    
    
    
]    