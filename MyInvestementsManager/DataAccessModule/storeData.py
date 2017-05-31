from MyInvestementsManager.models import ListedCompany,\
    DailyTradeSummary, DetailedTrade,\
    SectorIndex, SectorIndexNames, CompanyIssuedQuantitiesHistory
    
import datetime
from datetime import timedelta
import http
import json
from MyInvestementsManager.util.ApplicationConstants import URL_CSE,\
    FILE_TYPE_DATA_FILES, FILE_NAME_SECTOR_DATA_DOWNLOAD,\
    FILE_NAME_COMPANY_DATA_DOWNLOAD, FILE_NAME_TRADE_SUMMARY_DATA_DOWNLOAD,\
    FILE_NAME_DETAILED_TRADES_DATA_DOWNLOAD, URL_TRADE_SUMMARY_DATA_DOWNLOAD,\
    FILE_PATH_DATA

def persistCompaniesList(url) :
    """
    This method retrieves a list of symbols in the CSV format and create the models for each of them.
    If the symbol already exists following steps are taken.
    If the quantities of the symbol has been updated, update it on the database. And store the current status on the history table
    """
    symbolsToUpdate = getDataByHttps(URL_CSE, url)
    
    symbolsToUpdateJson = json.loads(symbolsToUpdate);
    
    
    for company in symbolsToUpdateJson['reqByMarketcap']:
        companyToSave, created = ListedCompany.objects.get_or_create(symbol = company['symbol'], 
                                                                        defaults = {'companyName' : company['name'], 
                                                                                    'price' : float(company['price'] or 0), 
                                                                                    'issuedQuentity' : int(company['issuedQTY'] or 0), 
                                                                                    'marketCapitalisation' : float(company['marketCap'] or 0), 
                                                                                    'marketCapitalisationPercentage' : float(company['marketCapPercentage'] or 0)},
                                                                        )
        if not created :
            if company['issuedQTY']  and companyToSave.issuedQuentity != int(company['issuedQTY']) :
                quantityHistory = CompanyIssuedQuantitiesHistory()
                quantityHistory.quantityDifference = companyToSave.issuedQuentity
                quantityHistory.marketCapitalisation = companyToSave.marketCapitalisation                
                quantityHistory.marketCapitalisationPercentage = companyToSave.marketCapitalisationPercentage
                quantityHistory.company = companyToSave
                quantityHistory.save()
                
            companyToSave.price = float(company['price'] or 0)
            companyToSave.issuedQuentity = int(company['issuedQTY'] or 0)
            companyToSave.marketCapitalisation = float(company['marketCap'] or 0)
            companyToSave.marketCapitalisationPercentage = float(company['marketCapPercentage'] or 0)
            companyToSave.save()
            
    saveFile(symbolsToUpdate, FILE_NAME_COMPANY_DATA_DOWNLOAD)
    
   
def clenupTodaysData():         
    today = datetime.date.today()
    
    #CSE trading summary
    DailyTradeSummary.objects.filter(date__range=(today, today + timedelta(1))).delete()
    
    #For other markets, data receives tow days later
    DailyTradeSummary.objects.filter(company__stockExchange = 'NYSE').filter(date__range=(today - timedelta(2), today - timedelta(1))).delete()
    DailyTradeSummary.objects.filter(company__stockExchange = 'NASDAQ').filter(date__range=(today - timedelta(2), today - timedelta(1))).delete()
    
    
def persistDailyTradingSummary():
    """
    Stores the daily trading summary information in the Database. if the data already exists for today, data is updated
    """
    tradingSummaryInformation = getDataByHttps(URL_CSE, URL_TRADE_SUMMARY_DATA_DOWNLOAD)  
    tradingSummaryInformationJson = json.loads(tradingSummaryInformation)
    
    #Skip the line with headers
    #$next(tradingSummaryInformation, None)
    

    
    for summary in tradingSummaryInformationJson['reqTradeSummery']:
        referencedCompany, created = ListedCompany.objects.get_or_create(symbol = summary['symbol'],
                                                                    defaults = {'companyName' : summary['name'], 
                                                                                    'price' : float(summary['price'] or 0),
                                                                                    'issuedQuentity' : 0,
                                                                                    'marketCapitalisation' : 0,
                                                                                    'marketCapitalisationPercentage' : 0})
        
        if referencedCompany :
            summaryToBeSaved = DailyTradeSummary(company = referencedCompany, date = datetime.datetime.strptime(summary['issueDate'], "%d/%b/%Y").date(), shareVolume = int(summary['sharevolume'] or 0), tradeVolume = int(summary['tradevolume'] or 0), turnover = float(summary['turnover'] or 0), high = float(summary['high'] or 0), low = float(summary['low'] or 0), priceChange = float(summary['change'] or 0), priceChangePercentage = float(summary['percentageChange'] or 0), lastTradedPrice = float(summary['closingPrice'] or 0), previouseClose = float(summary['previousClose'] or 0), open = float(summary['open'] or 0))
            summaryToBeSaved.save()

    saveFile(tradingSummaryInformation, FILE_PATH_DATA + '/CSE' + FILE_NAME_TRADE_SUMMARY_DATA_DOWNLOAD)
        



                                                                           
def persistDetailedTrades(url):
    """
    Stores the detailed trades information in the Database. if the data already exists for today, data is updated
    """
    detailedTrades = getDataByHttps(URL_CSE, url)
    
    detailedTradesJson = json.loads(detailedTrades)
    
    today = datetime.date.today()
    DetailedTrade.objects.filter(date__range=(today, today + timedelta(1))).delete()
    
    
    for item in detailedTradesJson['reqDetailTrades']:
        referencedCompany, created = ListedCompany.objects.get_or_create(symbol = item['symbol'],
                                                                    defaults = {'companyName' : item['name'], 
                                                                                    'price' : float(item['price'] or 0),
                                                                                    'issuedQuentity' : 0,
                                                                                    'marketCapitalisation' : 0,
                                                                                    'marketCapitalisationPercentage' : 0})
        
        if referencedCompany :
            detailedTradeToSave = DetailedTrade(company = referencedCompany, date = datetime.date.today(), tradeVolume = int(item['trades'] or 0), shareVolume = int(item['qty'] or 0), priceChange = float(item['change'] or 0), priceChangePercentage = float(item['changePercentage'] or 0))
            detailedTradeToSave.save()
        
    saveFile(detailedTrades, FILE_NAME_DETAILED_TRADES_DATA_DOWNLOAD)
        
def persistSectorIndices(url):
    """
    Stores the Sctors Indices information in the Database. if the data already exists for today, data is updated. The input is a html document. It shall be parsed to extract the correct data.
    """    
    sectorIndices = getDataByHttps(URL_CSE, url)  
    
    today = datetime.date.today()
    SectorIndex.objects.filter(date__range=(today, today + timedelta(1))).delete()
    
    sectorIndicesJson = json.loads(sectorIndices);
    
    #errorMessage = sectorIndicesJson.get('error', [])
    #if errorMessage:
    #    print('Error occured. No data recieved from exchange.')
    #    return
        
    for sectorIndex2 in sectorIndicesJson:
        print(sectorIndex2)
        for sectorIndex in sectorIndex2:
            print(sectorIndex)
            print(sectorIndex['name'])
            sectorName, created = SectorIndexNames.objects.get_or_create(name = sectorIndex['name'])
            
            if sectorName:
                sectorIndexToSave = SectorIndex(sector = sectorName, price = float(sectorIndex['indexValue']), value= float(sectorIndex['indexValue']), volume = int(getNumericalValue(sectorIndex['sectorVolumeToday'])), trades = int(getNumericalValue(sectorIndex['sectorTradeToday'] )), date = datetime.date.today())
                sectorIndexToSave.save()   
                
    
    saveFile(sectorIndices, FILE_NAME_SECTOR_DATA_DOWNLOAD)                                                      
                                      
                                      
#def loadLatestDataUnitedStates():
    
 #   print (getQuotes('AAPL'))     
                         
            
def saveFile(textContent, fileName, date = None):
    if date is None:
        date = datetime.date.today()
    dateStr = date.strftime('_%d_%m_%Y')
    text_file = open(fileName + dateStr + FILE_TYPE_DATA_FILES, 'w')
    
    text_file.write(textContent)
    text_file.close()
 
    
def getDataByHttps(exchngeUrl, url):
    conn = http.client.HTTPSConnection(exchngeUrl, 443)
    conn.putrequest('POST', url)
    conn.endheaders() # <---
    r = conn.getresponse()
    return r.read().decode('utf-8')


def getNumericalValue(val):
    if val and str(val).isdigit():
        return val
    else:
        return 0
    