import datetime
from collections import OrderedDict

from MyInvestementsManager.EODDataStoreModule.EOD_api import getLastTradedPrice


class DividendView:
    currentDivYeild = 0.0
    yearlyDividend = OrderedDict()
    company = None
    latestDividendDate = None
    dividendGrowthLastFiveYears = 0
    lastTradedPrice = 0

    def __str__(self):
        return "CurrentDivYeild : " + str(self.currentDivYeild) + " YearlyDividend: " + str(self.yearlyDividend) + " Company: " + str(
            self.company.symbol) + " Latest Div date: " + str(self.latestDividendDate) + " Growth Last 5 Years = " + str(
            self.dividendGrowthLastFiveYears) + " Last Traded Price: " + str(self.lastTradedPrice)


def getAggrigatedDividendData(dividends):
    group = groupByCompany(dividends)

    aggrigates = list()
    for company, dividends in group.items():
        dividends.sort(key=lambda dividend: dividend.entitled_date, reverse=True)
        divView = DividendView()
        divView.company = company

        lastTradedPrice = getLastTradedPrice(company)

        if lastTradedPrice:
            currentYear = datetime.date.today().year

            divView.dividendGrowthLastFiveYears = getDividendGrowth(dividends, currentYear - 5, currentYear)
            divView.lastTradedPrice = lastTradedPrice
            divView.latestDividendDate = dividends[0].entitled_date

            dividendByYear = getDividendForEachYear(dividends)
            divView.yearlyDividend = dividendByYear

            if (currentYear - 1) in dividendByYear:
                #Get last year's Dividend if there was a last year
                latestDividend = dividendByYear[currentYear - 1]
            else:
                #If not get the latest dividend
                latestDividend = dividendByYear.items()[0][1]

            divView.currentDivYeild = (latestDividend[0] / lastTradedPrice) * 100

        aggrigates.append(divView)

    aggrigates.sort(key=lambda aggrigate: aggrigate.currentDivYeild, reverse=True)
    return aggrigates


def groupByCompany(dividends):
    groupByCompany = OrderedDict()
    for dividend in dividends:
        if not groupByCompany.has_key(dividend.company):
            groupByCompany[dividend.company] = list()

        groupByCompany[dividend.company].append(dividend)
    return groupByCompany


def getDividendForEachYear(dividends):
    yearlyDiv = OrderedDict()
    for dividend in dividends:
        year = dividend.entitled_date.year
        if not yearlyDiv.has_key(year):
            total_div, total_scrip_div = getDividendCountForYear(dividends, year)
            yearlyDiv[year] = total_div, total_scrip_div
    return yearlyDiv


def getDividendCountForYear(dividends, year):
    divCount = 0
    scripDivCount = 0
    for dividend in dividends:
        if year == dividend.entitled_date.year:
            if dividend.type.name == 'SCRIP':
                scripDivCount += dividend.amountPerShare
            else:
                divCount += dividend.amountPerShare
    return divCount, scripDivCount


def getDividendGrowth(dividends, fromYear, toYear):
    dividendToYear = 0
    dividendFromYear = 0
    while (toYear > fromYear):
        dividendToYear = getDividendCountForYear(dividends, toYear)[0]

        if dividendToYear == 0:
            toYear = toYear - 1
        else:
            break

    while (toYear > fromYear):
        dividendFromYear = getDividendCountForYear(dividends, fromYear)[0]

        if dividendToYear == 0:
            fromYear = fromYear + 1
        else:
            break

    if dividendFromYear > 0:
        return ((dividendToYear - dividendFromYear) / dividendFromYear) * 100
    else:
        return 100