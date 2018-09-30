from MyInvestementsManager.currency.CurrencyConverter import valueInDefaultCurrency
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY
from MyInvestementsManager.models import DailyTradeSummary


def calculateAccumulatedInvestementData(investmentData):
    cumulativeDividendValue = 0.0
    context = {}
    
    for data in investmentData:
        cumulativeDividendValue = 0.0
        
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
        
                
            
        data.paidPrice = data.amount / data.quantity
        
            
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DailyTradeSummary.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    
    
    #Group by symbols
    investmentData = groupInvestmentDataBySymbol(investmentData)
    
    context['investDataBySymbol'] = investmentData
    # Calculate the total values of the investments
    totalValues = calculateTotalValuesOfInvestmentData(investmentData)
    
    context.update(totalValues)
    return context

def groupInvestmentDataBySymbol (investmentData):
    dataGroupedBySymbol = {}
    finalResult = []
    for data in investmentData:
        if data.investmentType.name != 'Equity':
            finalResult.append(data)
        else :
            symbol = data.symbol.symbol
            if symbol == 'NA':
                finalResult.append(data)
            else :
                dataForSymbol = dataGroupedBySymbol.get(symbol)
                if dataForSymbol is None:
                    #Calculate the dividends for the symbol
                    data.dividends = getCumulativeDividedsValueForTheInvestment(data)
                    
                    #Calculate the profit with dividends for the symbol
                    data.profitWithDividends = data.growth + data.dividends
                    if data.amount and float(data.amount) > 0:
                        data.growthPercentageWithDividends = (data.profitWithDividends) * 100 / data.amount
                    else :
                        data.growthPercentageWithDividends = 0
                        
                    dataGroupedBySymbol[symbol] = data
                else :
                    dataForSymbol.currentValue += data.currentValue
                    dataForSymbol.growth += data.growth
                    dataForSymbol.amount += data.amount
                    dataForSymbol.quantity += data.quantity
                    dataForSymbol.profitWithDividends += data.growth
                    
                    dataForSymbol.growthPercentage = (dataForSymbol.growth * 100) / dataForSymbol.amount
                    dataForSymbol.paidPrice = dataForSymbol.amount / dataForSymbol.quantity
                    dataForSymbol.growthPercentageWithDividends = (dataForSymbol.profitWithDividends * 100) / dataForSymbol.amount
    
    groupedEquities = list(dataGroupedBySymbol.values())
    finalResult += groupedEquities
    return finalResult;

def calculateTotalValuesOfInvestmentData(investmentData):
    totalAmount = 0.0
    totalCurrentValue = 0.0
    totalGrowth = 0.0
    totalEquityValue = 0.0
    totalBondValue = 0.0
    totalDividends = 0.0
    totalProfitWithDividends = 0.0
        
    context = {}
    
    for data in investmentData:
        totalAmount += data.amount
        totalCurrentValue += data.currentValue
        totalGrowth += data.growth
            
        if data.investmentType.name == 'Bond' :
            totalBondValue += data.currentValue
        elif data.investmentType.name == 'Equity':
            totalEquityValue += data.currentValue
            
        data.profitWithDividends = data.growth + data.dividends
        totalProfitWithDividends += data.profitWithDividends
        totalDividends += data.dividends 
            
    totalGrowhPercentage = (totalGrowth) * 100 / totalAmount
        
    context['totalAmount'] = totalAmount
    context['totalCurrentValue'] = totalCurrentValue 
    context['totalGrowth'] = totalGrowth
    context['totalGrowthPercentage'] = totalGrowhPercentage
    context['currency'] = DEFAULT_CURRENCY
    context['totalBondValue'] = totalBondValue
    context['totalEquityValue'] = totalEquityValue
    context['totalDividends'] = totalDividends
    context['totalProfitWithDividends'] = totalProfitWithDividends
    context['totalProfitPctWithDividends'] = totalProfitWithDividends * 100 / totalAmount
    
    return context

def calculateAccumulatedSectorData(sectorData):    
    totalValue = 0.0
    currentDate = sectorData[0].date.date()
    
    earliestSectorIndexes = {}
    latestSectorIndexes = []
    
    for data in sectorData:
        if data.date.date() == currentDate:
            earliestSectorIndexes[data.sector.name] = data.price
        else:
            latestSectorIndexes.append(data)
    
    for data in latestSectorIndexes:
        initialValue = earliestSectorIndexes[data.sector.name]
        growthPercentage = ((data.price - initialValue) / initialValue) * 100
        earliestSectorIndexes[data.sector.name] = growthPercentage
        
    latestSectorIndexes = [data for data in latestSectorIndexes if data.sector.name != 'ALL SHARE PRICE INDEX' and data.sector.name != 'SP SL20']
    
    latestSectorIndexes.sort(key=sortByPrice)
    
        
    context = {}
    
    context['cumilatedSectorValue'] = totalValue
    context['latestSectorIndexes'] = latestSectorIndexes
    context['sectorGrowthPercentage'] = earliestSectorIndexes 
    
    return context

def sortByPrice(item):
    return item.price

def getCumulativeDividedsValueForTheInvestment(data):
    #dividendsForInvestment = Devidends.objects.filter(investment = data)
    cumulativeDividendValue = 0
    #if(dividendsForInvestment):
     #   for dividend in dividendsForInvestment:
      #      cumulativeDividendValue += dividend.amount
    return cumulativeDividendValue