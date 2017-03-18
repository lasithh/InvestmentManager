from MyInvestementsManager.models import DetailedTrade,\
    CompanyFinanceReportSumary, ListedCompany
from django.utils.datastructures import OrderedSet
def getCompanyListWithHistoryData(companyData):
    context = {}
    
    
    
    #filter out all the intermediate reports and calculate the current EPS and PE value based on the new share price
    companiesList = OrderedSet()
    
    readHistoryData = False;
    for data in companyData:
        companiesList.add(data.company)
        if not readHistoryData:
            #load the history data for this symbol
            historyData = getCompanyHistoryData(data.company)
            context['historyData'] = historyData
            readHistoryData = True
                
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DetailedTrade.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    context['companiesList'] = companiesList
    return context


def getCompanyHistoryDataBySymbol (symbolToRead):
    
    companyToRead = ListedCompany.objects.filter(symbol = symbolToRead).first()
    return getCompanyHistoryData(companyToRead)

def getCompanyHistoryData (companyToRead):
    companyData = CompanyFinanceReportSumary.objects.filter(company = companyToRead).order_by('-issueDate')

    nextIndex = 1
    totalItems = companyData.count()

    
    for data in companyData:
        if data.type == 3 :
            data.earningsPerShare = (data.earningsPerShare * 4 ) / 3
            latestSharePrice = data.company.price
            data.PERatio = latestSharePrice / data.earningsPerShare
            
        if nextIndex < totalItems:
            if data.profitAfterTax > 0 :
                previousYearPAT = companyData[nextIndex].profitAfterTax
                patGrowthPercentage = ( (data.profitAfterTax - previousYearPAT) / previousYearPAT ) * 100
                data.patGrowthPercentage = patGrowthPercentage
            
            if data.earningsPerShare > 0 :
                previousYearEPS = companyData[nextIndex].earningsPerShare
                epsGrowthPercentage = ( (data.earningsPerShare - previousYearEPS) / previousYearEPS ) * 100
                data.epsGrowthPercentage = epsGrowthPercentage
                
            if data.PERatio > 0 :
                previousYearPERatio = companyData[nextIndex].PERatio
                peRatioGrowthPercentage = ( (data.PERatio - previousYearPERatio) / previousYearPERatio ) * 100
                data.peRatioGrowthPercentage = peRatioGrowthPercentage
            
            if data.devidendsPerShare > 0 :
                previousYearDPS = companyData[nextIndex].devidendsPerShare
                dpsGrowthPercentage = ( (data.devidendsPerShare - previousYearDPS) / previousYearDPS ) * 100
                data.dpsGrowthPercentage = dpsGrowthPercentage
                
            if data.assetsPerShare > 0 :
                previousYearNetAssets = companyData[nextIndex].assetsPerShare
                netAsetsGrowthPercentage = ( (data.assetsPerShare - previousYearNetAssets) / previousYearNetAssets ) * 100
                data.netAssetsGrowthPercentage = netAsetsGrowthPercentage
            
            nextIndex += 1
    
    return companyData