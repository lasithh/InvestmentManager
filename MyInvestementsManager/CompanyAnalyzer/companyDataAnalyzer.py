from MyInvestementsManager.models import DetailedTrade
def processCompanyHistoryData(companyData):
    context = {}
    
    for data in companyData:
        cumulativeDividendValue = 0.0
        
        #Perform the currency Conversion
        #data = valueInDefaultCurrency(data) no need yet
            
        #Set the current value based on teh symbol
        if data.symbol and data.symbol.symbol != 'NA' :
            data.currentValue = data.symbol.price * data.quantity
        else:
            data.currentValue = data.amount
                          
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DetailedTrade.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    
    return context
    