from MyInvestementsManager.currency.CurrencyConverter import valueInDefaultCurrency
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY
import datetime
from MyInvestementsManager.models import Dividends, DetailedTrade


def calculateAccumulatedInvestementData(investmentData):
    totalAmount = 0.0
    totalCurrentValue = 0.0
    totalGrowth = 0.0
    totalEquityValue = 0.0
    totalBondValue = 0.0
    totalDividends = 0.0
    totalProfitWithDividends = 0.0
    
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
                
        totalAmount += data.amount
        totalCurrentValue += data.currentValue
        totalGrowth += data.growth
            
        if data.investmentType.name == 'Bond' :
            totalBondValue += data.currentValue
        elif data.investmentType.name == 'Equity':
            totalEquityValue += data.currentValue
            
        data.paidPrice = data.amount / data.quantity
        
        dividendsForInvestment = Dividends.objects.filter(investment = data)
        
        if(dividendsForInvestment):
            for dividend in dividendsForInvestment:
                cumulativeDividendValue += dividend.amount
        
        data.dividends = cumulativeDividendValue
        data.profitWithDividends = data.growth + data.dividends
        
        totalProfitWithDividends += data.profitWithDividends
        
        totalDividends += cumulativeDividendValue
            
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
    
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DetailedTrade.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    
    
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