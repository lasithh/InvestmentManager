from django.shortcuts import render
from django.views.generic.list import ListView
from MyInvestementsManager.models import Investment, ListedCompany,\
    DailyTradeSummary, DetailedTrade, SectorIndex
    
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse

import urllib
from MyInvestementsManager.DataAccessModule.storeData import persistCompaniesList,\
    persistDailyTradingSummary, persistDetailedTrades, persistSectorIndices
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY
from MyInvestementsManager.currency.CurrencyConverter import valueInDefaultCurrency

# Create your views here.


def index(request):
    return render(request, 'MyInvestmentsManager/home.html')

#Define Views

#Investment related views 
class InvestmentsListView(ListView):
    model = Investment
    template_name='MyInvestmentsManager/investments_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(InvestmentsListView, self).get_context_data(**kwargs)
        
        totalAmount = 0.0
        totalCurrentValue = 0.0
        totalGrowth = 0.0
        totalEquityValue = 0.0
        totalBondValue = 0.0
        
        
        for data in context['object_list']:
            #Perform the currency Conversion
            data = valueInDefaultCurrency(data)
            
            #Set the current value based on teh symbol
            if data.symbol and data.symbol.symbol != 'NA' :
                data.currentValue = data.symbol.price * data.quantity
            else:
                data.currentValue = data.amount
                    
            data.growth = data.currentValue - data.amount
            
            
            
            if data.amount and float(data.amount) > 0:
                data.growthPercentage = (data.growth) * 100 / data.amount
            else :
                data.growthPercentage = 0
                
            totalAmount += data.amount
            totalCurrentValue += data.currentValue
            totalGrowth += data.growth
            
            if data.investmentType.name == 'Bond' :
                totalBondValue += data.currentValue
            elif data.investmentType.name == 'Equity':
                totalEquityValue += data.currentValue
        
        totalGrowhPercentage = (totalGrowth) * 100 / totalAmount
        
        context['totalAmount'] = totalAmount
        context['totalCurrentValue'] = totalCurrentValue 
        context['totalGrowth'] = totalGrowth
        context['totalGrowthPercentage'] = totalGrowhPercentage
        context['currency'] = DEFAULT_CURRENCY
        
        context['totalBondValue'] = totalBondValue
        context['totalEquityValue'] = totalEquityValue
        
        return context
    
class InvestementDetailView(DetailView):
    model = Investment    

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
    fields = ['name', 'amount', 'investmentType', 'symbol', 'quantity', 'currentValue']
    def get_success_url(self):
        return reverse('index')
    
class InvestmentCreateView(CreateView):
    model = Investment
    template_name="MyInvestmentsManager/add_investment.html"
    fields = ['name', 'amount', 'investmentType', 'symbol', 'quantity', 'currentValue']
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

