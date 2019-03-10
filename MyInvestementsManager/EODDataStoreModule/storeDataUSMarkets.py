from MyInvestementsManager.EODDataStoreModule.storeData import getDataByHttps,\
    saveFile
from MyInvestementsManager.util.ApplicationConstants import URL_NASDQ,\
    URL_TRADE_SUMMARY_DATA_DOWNLOAD_NASDQ, FILE_NAME_TRADE_SUMMARY_DATA_DOWNLOAD,\
    FILE_PATH_DATA, URL_NYSE, URL_TRADE_SUMMARY_DATA_DOWNLOAD_NYSE
from MyInvestementsManager.models import ListedCompany, DailyTradeSummary
import datetime
from datetime import timedelta
def persistDailyTradingSummary_US(date  = datetime.date.today() - timedelta(2)):
    """
    Stores the daily trading summary information in the Database. if the data already exists for today, data is updated
    """
    tradeSummaryURL = URL_TRADE_SUMMARY_DATA_DOWNLOAD_NASDQ.format(date.day, date.month, date.year)
    
    tradingSummaryInformation = getDataByHttps(URL_NASDQ, tradeSummaryURL)  
    storeDailyTradinSummaryData(tradingSummaryInformation, "NASDQ", date)
    
    tradeSummaryURL = URL_TRADE_SUMMARY_DATA_DOWNLOAD_NYSE.format(date.day, date.month, date.year)
    
    tradingSummaryInformation = getDataByHttps(URL_NYSE, tradeSummaryURL)  
    storeDailyTradinSummaryData(tradingSummaryInformation, "NYSE", date)
    
def storeDailyTradinSummaryData(dailyTradingSummaryData, exchange, date): 
    for dailySummary in dailyTradingSummaryData.split() :
        data = dailySummary.split(";")
        #Format of data symbol,open,high,low,last,volume,value
        referencedCompany, created = ListedCompany.objects.get_or_create(symbol = data[0],
                                                                    defaults = { 'price' : float(data[4] or 0),
                                                                                 'stockExchange' : exchange,
                                                                                 'issuedQuentity' : 0,
                                                                                 'marketCapitalisation' : 0,
                                                                                 'marketCapitalisationPercentage' : 0,
                                                                                 
                                                                                })
        
        if referencedCompany :
            summaryToBeSaved = DailyTradeSummary(company = referencedCompany, date = date, tradeVolume = int(data[5] or 0), turnover = float(data[6] or 0), high = float(data[2] or 0), low = float(data[3] or 0), lastTradedPrice = float(data[4] or 0), open = float(data[1] or 0), shareVolume = 0, previouseClose = 0, priceChange = 0, priceChangePercentage = 0)
            summaryToBeSaved.save()
            
    saveFile(dailyTradingSummaryData, FILE_PATH_DATA + '/' + exchange + FILE_NAME_TRADE_SUMMARY_DATA_DOWNLOAD)
        