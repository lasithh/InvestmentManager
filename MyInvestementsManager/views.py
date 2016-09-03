from django.shortcuts import render
from django.views.generic.list import ListView
from MyInvestementsManager.models import Investment, ListedCompany,\
    DailyTradeSummary, DetailedTrade, SectorIndex
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse

import urllib
from MyInvestementsManager.DataAccessModule.storeData import persistCompaniesList,\
    persistDailyTradingSummary, persistDetailedTrades, persistSectorIndices
import datetime
# Create your views here.


def index(request):
    return render(request, 'MyInvestmentsManager/home.html')

#Define Views

#Investment related views 
class InvestmentsListView(ListView):
    model = Investment
    template_name='MyInvestmentsManager/investments_list.html'
    
class InvestementDetailView(DetailView):
    model = Investment    
    
class InvestmentCreateView(CreateView):
    model = Investment
    fields = ['name', 'amount', 'date']
    template_name = 'MyInvestmentsManager/add_investment.html'
    def get_success_url(self):
        return reverse('add_investment')

class InvestmentDetailView(DetailView):
    model = Investment
    template_name = "MyInvestmentsManager/view_investment.html"
    
class InvestmentDeleteView(DeleteView):
    model = Investment
    template_name="MyInvestmentsManager/investment_confirm_delete.html"
    def get_success_url(self):
        return reverse('index')
    
class InvestmentUpdateView(UpdateView):
    model = Investment
    template_name="MyInvestmentsManager/update_investment.html"
    fields = ['name', 'amount', 'date']
    def get_success_url(self):
        return reverse('index')
    


#Symbols related views    
class ListedCompanyListView(ListView):
    model = ListedCompany
    template_name='MyInvestmentsManager/company/companies_list.html'
    
class ListedCompanyView(DetailView):
    model = ListedCompany
    template_name = "MyInvestmentsManager/company/view_company.html"
    
def updateSymbolsList(request):
    response = urllib.request.urlopen('http://www.cse.lk/marketcap_report.do?reportType=CSV')
    
    persistCompaniesList(response)
    
    return HttpResponse("Success")



#Daily Trading summary related views

class DailyTradingSummaryListView(ListView):
    model = DailyTradeSummary
    template_name='MyInvestmentsManager/dalilyTradingSummary/daily_trading_summary_list.html'
    
class DailyTradingSummaryView(DetailView):
    model = DailyTradeSummary
    template_name = "MyInvestmentsManager/dalilyTradingSummary/view_daily_trading_summary.html"

def storeDailyTradingSummary(request):
    response = urllib.request.urlopen('http://www.cse.lk/trade_summary_report.do?reportType=CSV')
    
    persistDailyTradingSummary(response)
    
    return HttpResponse("Success")


#Detailed trades related views
class DetailedTradeListView(ListView):
    model = DetailedTrade
    template_name='MyInvestmentsManager/detailedTrades/detailed_trades_list.html'
    
class DetailedTradeView(DetailView):
    model = DetailedTrade
    template_name = "MyInvestmentsManager/detailedTrades/view_detailed_trade.html"

def storeDetailedTrades(request):
    response = urllib.request.urlopen('http://www.cse.lk/detail_trades_report.do?reportType=CSV')
    
    persistDetailedTrades(response)
    
    return HttpResponse("Success")


#Stock Indices Related URLs
class SectorIndexListView(ListView):
    model = SectorIndex
    template_name='MyInvestmentsManager/sectorIndices/sector_indices_list.html'
    
class SectorIndexView(DetailView):
    model = SectorIndex
    template_name = "MyInvestmentsManager/sectorIndices/view_sector_index.html"

def storeSectorIndices(request):
    response = urllib.request.urlopen('https://www.cse.lk/indices.do')
    
    persistSectorIndices(response)
    
    return HttpResponse("Success")

