from MyInvestementsManager.DividendsManager.dividend_api import get_div_data
from MyInvestementsManager.EODDataStoreModule.EOD_api import getLastTradedPrice
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY
from MyInvestementsManager.models import DailyTradeSummary, Investment


def calculateAccumulatedInvestementData(investmentData):
    context = {}
    
    for data in investmentData:
        data.currentValue = data.symbol.price * data.quantity
        data.growth = data.currentValue - data.amount
        data.paidPrice = data.amount / data.quantity

        #calculate dividends
        data.dividends = calculateDividends(data)
        data.profitWithDividends = data.growth + data.dividends

            
    #Get the last updated date of the data --> select the last updated Trade Summary and get the date
    latestDetailedTrade = DailyTradeSummary.objects.latest('date')
    context['lastUpdateDate'] = latestDetailedTrade.date
    
    
    #Group by symbols
    investmentData = groupInvestmentDataBySymbol(investmentData)

    #Sort the list
    investmentData = sorted(investmentData, key=lambda x: x.symbol.symbol)
    
    context['investDataBySymbol'] = investmentData
    # Calculate the total values of the investments
    totalValues = calculateTotalValuesOfInvestmentData(investmentData)
    
    context.update(totalValues)
    return context


def groupInvestmentDataBySymbol (investmentData):
    data_grouped_by_symbol = {}
    final_result = []
    for data in investmentData:
        symbol = data.symbol.symbol
        data_for_symbol = data_grouped_by_symbol.get(symbol)
        if data_for_symbol is None:

            # Create empty object
            data_for_symbol = Investment()

            # Set the symbol
            data_for_symbol.symbol = data.symbol
            data_for_symbol.investmentType = data.investmentType
            data_for_symbol.name = data.name

            # Initialize with 0 values
            data_for_symbol.currentValue = 0
            data_for_symbol.growth = 0
            data_for_symbol.amount = 0
            data_for_symbol.quantity = 0
            data_for_symbol.profitWithDividends = 0
            data_for_symbol.growthPercentage = 0
            data_for_symbol.paidPrice = 0
            data_for_symbol.growthPercentageWithDividends = 0
            data_for_symbol.dividends = 0


            #Add it to the map
            data_grouped_by_symbol[symbol] = data_for_symbol

        #Accumulate individual investment data in to a single investment object
        data_for_symbol.currentValue += data.currentValue
        data_for_symbol.growth += data.growth
        data_for_symbol.amount += data.amount
        data_for_symbol.quantity += data.quantity
        data_for_symbol.dividends += data.dividends
        data_for_symbol.profitWithDividends += data.profitWithDividends

        data_for_symbol.growthPercentage = (data_for_symbol.growth * 100) / data_for_symbol.amount
        data_for_symbol.paidPrice = data_for_symbol.amount / data_for_symbol.quantity
        data_for_symbol.growthPercentageWithDividends = (data_for_symbol.profitWithDividends * 100) / data_for_symbol.amount
    
    grouped_equities = list(data_grouped_by_symbol.values())
    final_result += grouped_equities
    return final_result


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


def calculateDividends(investment):
    dividends = get_div_data(investment.symbol)
    total_dividend = 0
    last_traded_price = getLastTradedPrice(investment.symbol)
    for dividend in dividends:
        #If dividend was offered after you made the investment
        if investment.date <= dividend.entitled_date:
            if dividend.type.name == 'SCRIP':
                total_dividend += dividend.amountPerShare * investment.quantity * last_traded_price
            else:
                if investment.symbol == 'ALLI.N0000':
                    print (dividend)
                    print (investment)

                total_dividend += dividend.amountPerShare * investment.quantity
    return total_dividend
