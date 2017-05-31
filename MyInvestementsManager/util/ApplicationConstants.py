import enum
from MyInvestementsManager.util import ExchangeInformation
DEFAULT_CURRENCY = "LKR"

FILE_TYPE_DATA_FILES = '.txt'

URL_NET_FONDS = "www.netfonds.no"

#Trade Summary Constants
TRADE_SUMMARY_SYMBOL = "symbol"
TRADE_SUMMARY_COMPANY_NAME="companyName"
TRADE_SUMMARY_PRICE="price"
TRADE_SUMMARY_LAST_TRADED_PRICE="lastTradedprice"
TRADE_SUMMARY_DATE = "date"
TRADE_SUMMARY_DATE_FORMAT= "dateFormat"
TRADE_SUMMARY_SHARE_VOLUME="volume"
TRADE_SUMMARY_TRADE_VOLUME="tradeVolume"
TRADE_SUMMARY_TURNOVER="turnover"
TRADE_SUMMARY_HIGH="high"
TRADE_SUMMARY_LOW="low"
TRADE_SUMMARY_PRICE_CHANGE="priceChange"
TRADE_SUMMARY_PRICE_CHANGE_PCT="percentageChange"
TRADE_SUMMARY_PREVIOUS_CLOSE="previousClose"
TRADE_SUMMARY_OPEN="open"



#Trade summary CSV format
TRADE_SUMMARY_FORMAT_CSE = {
    TRADE_SUMMARY_SYMBOL : "symbol",
    TRADE_SUMMARY_COMPANY_NAME : "name",
    TRADE_SUMMARY_PRICE : "price",
    TRADE_SUMMARY_LAST_TRADED_PRICE : "closingPrice",
    TRADE_SUMMARY_DATE : "issueDate",
    TRADE_SUMMARY_DATE_FORMAT : "%d/%b/%Y",
    TRADE_SUMMARY_SHARE_VOLUME : "sharevolume",
    TRADE_SUMMARY_TRADE_VOLUME : "tradevolume",
    TRADE_SUMMARY_TURNOVER : "turnover",
    TRADE_SUMMARY_HIGH : "high",
    TRADE_SUMMARY_LOW : "low",
    TRADE_SUMMARY_PRICE_CHANGE : "change",
    TRADE_SUMMARY_PRICE_CHANGE_PCT : "percentageChange",
    TRADE_SUMMARY_PREVIOUS_CLOSE : "previousClose",
    TRADE_SUMMARY_OPEN : "open"
}


#meta data for CSE
URL_CSE = 'www.cse.lk'
FILE_PATH_DATA = 'data'


URL_SECTOR_DATA_DOWNLOAD = '/api/marketIndices'
FILE_NAME_SECTOR_DATA_DOWNLOAD = FILE_PATH_DATA + '/sector/sector_data'

URL_TRADE_SUMMARY_DATA_DOWNLOAD = '/api/tradeSummary'
FILE_NAME_TRADE_SUMMARY_DATA_DOWNLOAD = '/trade_summary/trade_summary'

URL_COMPANY_DATA_DOWNLOAD = '/api/list_by_market_cap'
FILE_NAME_COMPANY_DATA_DOWNLOAD = FILE_PATH_DATA + '/company/company_data'

URL_DETAILED_TRADES_DATA_DOWNLOAD = '/api/detailedTrades'
FILE_NAME_DETAILED_TRADES_DATA_DOWNLOAD = FILE_PATH_DATA + '/detailed_trades/detailed_trades_data'


#Trade summary CSV format
TRADE_SUMMARY_FORMAT_CSE = {
    TRADE_SUMMARY_SYMBOL : "symbol",
    TRADE_SUMMARY_COMPANY_NAME : "name",
    TRADE_SUMMARY_PRICE : "price",
    TRADE_SUMMARY_LAST_TRADED_PRICE : "closingPrice",
    TRADE_SUMMARY_DATE : "issueDate",
    TRADE_SUMMARY_DATE_FORMAT : "%d/%b/%Y",
    TRADE_SUMMARY_SHARE_VOLUME : "sharevolume",
    TRADE_SUMMARY_TRADE_VOLUME : "tradevolume",
    TRADE_SUMMARY_TURNOVER : "turnover",
    TRADE_SUMMARY_HIGH : "high",
    TRADE_SUMMARY_LOW : "low",
    TRADE_SUMMARY_PRICE_CHANGE : "change",
    TRADE_SUMMARY_PRICE_CHANGE_PCT : "percentageChange",
    TRADE_SUMMARY_PREVIOUS_CLOSE : "previousClose",
    TRADE_SUMMARY_OPEN : "open"
}


#Meta data for NASDQ

URL_NASDQ = URL_NET_FONDS

URL_TRADE_SUMMARY_DATA_DOWNLOAD_NASDQ="/quotes/exchange.php?exchange=O&at_day={0}&at_month={1}&at_year={2}&format=csv"

URL_NYSE = URL_NET_FONDS

URL_TRADE_SUMMARY_DATA_DOWNLOAD_NYSE="/quotes/exchange.php?exchange=N&at_day={0}&at_month={1}&at_year={2}&format=csv"
