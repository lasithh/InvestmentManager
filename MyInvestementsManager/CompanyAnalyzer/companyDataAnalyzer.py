from MyInvestementsManager.models import DetailedTrade,\
    CompanyFinanceReportSumary, ListedCompany, DailyTradeSummary
from django.utils.datastructures import OrderedSet
import copy
import datetime

def getCompanyListWithHistoryData(companyData):
    context = {}
    #filter out all the intermediate reports and calculate the current EPS and PE value based on the new share price
    companiesList = OrderedSet()
    
    readHistoryData = False;
    for data in companyData:
        companiesList.add(data.company)
        if not readHistoryData:
            #load the history data for this symbol
            historyData = getCompanyHistoryDataByCompany(data.company)
            context['historyData'] = historyData
            readHistoryData = True
                
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DailyTradeSummary.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    context['companiesList'] = companiesList
    return context

def getCompanyHistoryDataByCompany (companyToRead):
    companyData = CompanyFinanceReportSumary.objects.filter(company = companyToRead).order_by('-issueDate')
    calculatedFinancialHistoryData = getCompanyHistoryData(companyData)
   # calculatedFinancialHistoryData = addTheRecordWithCurrentPriceAndValue

def getCompanyHistoryData (companyData):
    calculateNonExistingFinancialDataValues (companyData);
    
    annualReportsList = list()
    
    latestData = populateCurrentFinancialStatus(companyData)
    print(latestData.profitAfterTax)
    
    annualReportsList.append(latestData)
    #filter annual reports
    for data in companyData:
        if data.type == 0:
            annualReportsList.append(data)
    
    totalItems = len(annualReportsList)
    
    nextIndex = 1
    for data in annualReportsList:
        if nextIndex < totalItems:
            if data.profitAfterTax > 0 :
                previousYearPAT = annualReportsList[nextIndex].profitAfterTax
                patGrowthPercentage = ( (data.profitAfterTax - previousYearPAT) / previousYearPAT ) * 100
                data.patGrowthPercentage = patGrowthPercentage
            
            if data.earningsPerShare > 0 :
                previousYearEPS = annualReportsList[nextIndex].earningsPerShare
                epsGrowthPercentage = ( (data.earningsPerShare - previousYearEPS) / previousYearEPS ) * 100
                data.epsGrowthPercentage = epsGrowthPercentage
                
            if data.PERatio > 0 :
                previousYearPERatio = annualReportsList[nextIndex].PERatio
                if previousYearPERatio > 0:
                    peRatioGrowthPercentage = ( (data.PERatio - previousYearPERatio) / previousYearPERatio ) * 100
                    data.peRatioGrowthPercentage = peRatioGrowthPercentage
            
            if data.devidendsPerShare > 0 :
                previousYearDPS = annualReportsList[nextIndex].devidendsPerShare
                if previousYearDPS > 0 :
                    dpsGrowthPercentage = ( (data.devidendsPerShare - previousYearDPS) / previousYearDPS ) * 100
                    data.dpsGrowthPercentage = dpsGrowthPercentage
                
            if data.assetsPerShare > 0 :
                previousYearNetAssets = annualReportsList[nextIndex].assetsPerShare
                netAsetsGrowthPercentage = ( (data.assetsPerShare - previousYearNetAssets) / previousYearNetAssets ) * 100
                data.netAssetsGrowthPercentage = netAsetsGrowthPercentage
            
            if data.devidendsPerShare > 0 and data.sharePrice > 0:
                data.devidendsYeild = (data.devidendsPerShare / data.sharePrice) * 100
            nextIndex += 1
    
    return annualReportsList


def populateCurrentFinancialStatus(companyData):
    latestRecord = copy.deepcopy(companyData[0])
    latestRecord.issueDate = datetime.date.today()
    
    #estimate the EPS value for the whole year based on the current EPS value
    estimatedEPS= calculateEstimatedEPS(latestRecord.earningsPerShare, latestRecord.type)
    
    latestRecord.earningsPerShare = estimatedEPS
    latestSharePrice = latestRecord.company.price
    latestRecord.PERatio = latestSharePrice / latestRecord.earningsPerShare
    latestRecord.sharePrice = latestSharePrice
    
    return latestRecord
    

def calculateEstimatedEPS(currentEPS, reportType):
    estimatedEPS = currentEPS
    
    #third quarter
    if reportType == 3 :
        estimatedEPS = (currentEPS * 4) / 3
    else :
        #first quarter
        if reportType == 1:
            estimatedEPS = currentEPS * 4
        else:
            #second quarter
            if reportType == 2:
                estimatedEPS = currentEPS * 2
                   
    return estimatedEPS
    
    
def calculateNonExistingFinancialDataValues(companyData):
    for data in companyData:
        if data.PERatio <= 0:
            calculatedPERatio = data.sharePrice / data.earningsPerShare
            data.PERatio = calculatedPERatio
            
        if data.devidendsPerShare <= 0 and data.numberOfShares > 0:
            calculatedDPS = data.grossDividends / data.numberOfShares
            data.devidendsPerShare = calculatedDPS
