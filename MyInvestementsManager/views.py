from django.shortcuts import render
from django.views.generic.list import ListView

from MyInvestementsManager.DividendsManager.dividend_api import retrieve_store_latest_dividends, \
    getAggrigatedDividendData, retrieve_aggrigated_div_data
from MyInvestementsManager.DividendsManager.dividend_extractor import read_latest_dividends
from MyInvestementsManager.models import Investment, ListedCompany,\
    DailyTradeSummary, DetailedTrade, SectorIndex, SectorIndexNames, Dividend,\
    CompanyFinanceReportSumary
    
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse

from MyInvestementsManager.EODDataStoreModule.storeData import persistCompaniesList,\
    persistDailyTradingSummary, persistDetailedTrades, persistSectorIndices,\
    clenupTodaysData
from MyInvestementsManager.util.ApplicationConstants import URL_SECTOR_DATA_DOWNLOAD, URL_COMPANY_DATA_DOWNLOAD,\
    URL_DETAILED_TRADES_DATA_DOWNLOAD
from MyInvestementsManager.DataProcessor.dataProcessor import calculateAccumulatedInvestementData,\
    calculateAccumulatedSectorData
from datetime import datetime
from django.db.models.query_utils import Q
from datetime import timedelta
from MyInvestementsManager.CompanyAnalyzer.companyDataAnalyzer import getCompanyListWithHistoryData,\
    getCompanyHistoryData
from MyInvestementsManager.forms import CompanyFinanceReportSumaryForm


# Create your views here.


def index(request):
    return render(request, 'MyInvestmentsManager/home.html')

#Define Views

#Investment related views 
class InvestmentsListView(ListView):
    model = Investment
    template_name='MyInvestmentsManager/investments_list.html'
    
    def get_context_data(self, **kwargs):
        #Get the context object
        context = super(InvestmentsListView, self).get_context_data(**kwargs)
        
        #Calculate the accumulated data 
        processedData= calculateAccumulatedInvestementData(context['object_list'])
        context.update(processedData)

        return context


class DividendListView(ListView):
    model = Dividend
    template_name = 'MyInvestmentsManager/dividend/dividends_list.html'

    def get_context_data(self, **kwargs):
        # Get the context object
        context = super(DividendListView, self).get_context_data(**kwargs)

        # Calculate the accumulated data
        agg_dividends = retrieve_aggrigated_div_data(context['object_list'])
        context['divAggData'] = agg_dividends

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
    fields = ['name', 'amount', 'investmentType', 'symbol', 'quantity', 'currentValue', 'date']
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
    #PErsists data to the database
    persistCompaniesList(URL_COMPANY_DATA_DOWNLOAD)
    
    return HttpResponse("Success")

#Daily Trading summary related views
class DailyTradingSummaryListView(ListView):
    model = DailyTradeSummary
    template_name='MyInvestmentsManager/dalilyTradingSummary/daily_trading_summary_list.html'
    
class DailyTradingSummaryView(DetailView):
    model = DailyTradeSummary
    template_name = "MyInvestmentsManager/dalilyTradingSummary/view_daily_trading_summary.html"

def storeDailyTradingSummary(request):
    #Store data on the database
    persistDailyTradingSummary()
    
    return HttpResponse("Success")


#Detailed trades related views
class DetailedTradeListView(ListView):
    model = DetailedTrade
    template_name='MyInvestmentsManager/detailedTrades/detailed_trades_list.html'
    
class DetailedTradeView(DetailView):
    model = DetailedTrade
    template_name = "MyInvestmentsManager/detailedTrades/view_detailed_trade.html"

def storeDetailedTrades(request):
    #Store in the database
    persistDetailedTrades(URL_DETAILED_TRADES_DATA_DOWNLOAD)
    
    return HttpResponse("Success")

#Stock Indices Related URLs
class SectorIndexListView(ListView):
    model = SectorIndex
    template_name='MyInvestmentsManager/sectorIndices/sector_indices_list.html'
    
    def get_queryset(self):
        #min_date = SectorIndex.objects.earliest('date').date.date()
        min_date = datetime(2016, 9, 5).date()
        min_date_end = min_date + timedelta(days=1)
        
        max_date = SectorIndex.objects.latest('date').date.date()
        
        #return SectorIndex.objects.filter(date__range = [max_date, datetime.today()])
        return SectorIndex.objects.filter(Q(date__range=(min_date, min_date_end)) | Q(date__range=(max_date, datetime.today()))).order_by('date')
    
    def get_context_data(self, **kwargs):
        #Get the context object
        context = super(SectorIndexListView, self).get_context_data(**kwargs)
        
        sectorNameNew = SectorIndexNames.objects.filter(name='POWER & ENERGY').first()
        sectorNameOld = SectorIndexNames.objects.filter(name='POWER  ENERGY').first()
        
        SectorIndex.objects.filter(sector=sectorNameOld).update(sector=sectorNameNew)
        
        #Calculate the accumulated data 
        cumilatedSectorValues = calculateAccumulatedSectorData(context['object_list'])
        context.update(cumilatedSectorValues)

        return context
    
    
class SectorIndexView(DetailView):
    model = SectorIndex
    template_name = "MyInvestmentsManager/sectorIndices/view_sector_index.html"
    
class DividendsCreateView(CreateView):
    model = Dividend
    fields = ['investment', 'amount']
    template_name = 'MyInvestmentsManager/dividend/add_dividend.html'

    def form_valid(self, form):
        form.instance.env = Investment.objects.get(pk=self.kwargs['investmentId'])
        return super(DividendsCreateView, self).form_valid(form)

#Company financial data related views
class CompaniesWithFinanceReportSumaryListView(ListView):
    model = CompanyFinanceReportSumary
    template_name='MyInvestmentsManager/companyFinanceSummary/company_finance_summary_list.html'
    
    def get_queryset(self):
        return CompanyFinanceReportSumary.objects.order_by('-issueDate')
    
    def get_context_data(self, **kwargs):
        #Get the context object
        context = super(CompaniesWithFinanceReportSumaryListView, self).get_context_data(**kwargs)
        
        #Calculate the accumulated data 
        processedData= getCompanyListWithHistoryData(context['object_list'])
        context.update(processedData)

        return context
    
#Company financial data related views
class CompanyFinanceReportSumaryListView(ListView):
    model = CompanyFinanceReportSumary
    template_name='MyInvestmentsManager/companyFinanceSummary/company_finance_summary_table.html'
    
    def get_queryset(self):
        symbolToRead = self.request.GET.get('symbol')
        company = ListedCompany.objects.filter(symbol = symbolToRead).first()
        return CompanyFinanceReportSumary.objects.filter(company = company).order_by('-issueDate')
    
    def get_context_data(self, **kwargs):
        #Get the context object
        context = super(CompanyFinanceReportSumaryListView, self).get_context_data(**kwargs)
        
        #Calculate the accumulated data 
        processedData= getCompanyHistoryData(context['object_list'])
        context['historyData'] = processedData;

        return context

class CompanyFinanceReportSumaryCreateView(CreateView):
    form_class = CompanyFinanceReportSumaryForm
    model = CompanyFinanceReportSumary
    template_name="MyInvestmentsManager/companyFinanceSummary/add_company_finance_summary.html"
              
    def get_success_url(self):
        return reverse('index')

def storeSectorIndices(request):
    #Store data on the database    
    persistSectorIndices(URL_SECTOR_DATA_DOWNLOAD)
  
    return HttpResponse("Success")

def loadLatestData(request):
    retrieve_store_latest_dividends()

    #storeSectorIndices(request)
    
    #updateSymbolsList(request)
    
    #clenupTodaysData()
    
    #storeDailyTradingSummary(request)
    
    #storeDetailedTrades(request)

    #persistDailyTradingSummary_US()
    
    return HttpResponse("Success")

