from MyInvestementsManager.currency.CurrencyConverter import valueInDefaultCurrency
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY
import datetime


def calculateAccumulatedInvestementData(investmentData):
    totalAmount = 0.0
    totalCurrentValue = 0.0
    totalGrowth = 0.0
    totalEquityValue = 0.0
    totalBondValue = 0.0
        
    context = {}
    
    for data in investmentData:
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


def calculateAccumulatedSectorData(sectorData):    
    totalValue = 0.0
    
    for data in sectorData:
        totalValue += data.value
    
    return totalValue