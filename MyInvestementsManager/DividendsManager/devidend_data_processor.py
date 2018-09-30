import datetime

from MyInvestementsManager.EODDataStoreModule.EOD_api import getLastTradedPrice


class DividendView:
    currentDivYeild = 0.0
    lastYerTotalDividend = 0.0
    numberOfDividends = 0
    company = None
    latestDividendDate = None
    dividendGrowthLastFiveYears = 0
    lastTradedPrice = 0

def getAggrigatedDividendData(dividends):
    group =  groupByCompany(dividends)

    aggrigates = list()
    for company, dividends in group.items():
        dividends.sort(key=lambda dividend: dividend.entitled_date, reverse=True)
        divView = DividendView()
        divView.company = company
        divView.numberOfDividends = len(dividends)

        lastTradedPrice = getLastTradedPrice(company)

        if lastTradedPrice:
            currentYear = datetime.date.today().year
            thisYearDividend = getDividendCountForYear(dividends, currentYear, lastTradedPrice)

            divView.currentDivYeild = (thisYearDividend / lastTradedPrice) * 100
            divView.lastYerTotalDividend = getDividendCountForYear(dividends, currentYear - 1, lastTradedPrice)
            divView.dividendGrowthLastFiveYears = getDividendGrowth(dividends, currentYear - 5, currentYear, lastTradedPrice)
            divView.lastTradedPrice = lastTradedPrice
            divView.latestDividendDate = dividends[0].entitled_date

        aggrigates.append(divView)

    aggrigates.sort(key=lambda aggrigate: aggrigate.currentDivYeild, reverse=True)
    return aggrigates

def groupByCompany(dividends):
    groupByCompany = dict()
    for dividend in dividends:
        if not groupByCompany.has_key(dividend.company):
            groupByCompany[dividend.company] = list()

        groupByCompany[dividend.company].append(dividend)
    return groupByCompany


def getDividendCountForYear(dividends, year, lastTradePrice):
    divCount = 0;
    for dividend in dividends:
        if year == dividend.entitled_date.year:
            if dividend.type.name == 'SCRIP':
                divCount += ((1 / dividend.amountPerShare) * lastTradePrice)
            else:
                divCount += dividend.amountPerShare
    return divCount

def getDividendGrowth(dividends, fromYear, toYear, lastTradedPrice):
    dividendToYear = 0
    dividendFromYear = 0
    while (toYear > fromYear):
        dividendToYear = getDividendCountForYear(dividends, toYear, lastTradedPrice)

        if dividendToYear == 0:
            toYear = toYear - 1
        else:
            break

    while (toYear > fromYear):
        dividendFromYear = getDividendCountForYear(dividends, fromYear, lastTradedPrice)

        if dividendToYear == 0:
            fromYear = fromYear + 1
        else:
            break

    if dividendFromYear > 0:
        return ((dividendToYear - dividendFromYear) / dividendFromYear) * 100
    else:
        return 100