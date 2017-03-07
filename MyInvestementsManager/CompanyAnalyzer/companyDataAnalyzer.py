from MyInvestementsManager.models import DetailedTrade
def processCompanyHistoryData(companyData):
    context = {}
    
    nextIndex = 1
    totalItems = companyData.count()
    
    for data in companyData:
        if nextIndex < totalItems :
            previousYearPAT = companyData[nextIndex].profitAfterTax
            patGrowthPercentage = ( (data.profitAfterTax - previousYearPAT) / previousYearPAT ) * 100
            data.patGrowthPercentage = patGrowthPercentage
            
            previousYearEPS = companyData[nextIndex].earningsPerShare
            epsGrowthPercentage = ( (data.earningsPerShare - previousYearEPS) / previousYearEPS ) * 100
            data.epsGrowthPercentage = epsGrowthPercentage
            
            previousYearPERatio = companyData[nextIndex].PERatio
            peRatioGrowthPercentage = ( (data.PERatio - previousYearPERatio) / previousYearPERatio ) * 100
            data.peRatioGrowthPercentage = peRatioGrowthPercentage
            
            previousYearDPS = companyData[nextIndex].devidendsPerShare
            dpsGrowthPercentage = ( (data.devidendsPerShare - previousYearDPS) / previousYearDPS ) * 100
            data.dpsGrowthPercentage = dpsGrowthPercentage
            
            nextIndex += 1
        #Perform the currency Conversion
        #data = valueInDefaultCurrency(data) no need yet
            
                          
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DetailedTrade.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    context['company'] = companyData[0].company
    
    return context
    