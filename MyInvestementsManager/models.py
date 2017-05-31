from django.db import models

# Create your models here.
class ListedCompany(models.Model):
    companyName = models.CharField(max_length = 250)
    symbol = models.CharField(max_length = 20)
    price = models.FloatField()
    issuedQuentity = models.BigIntegerField()
    marketCapitalisation = models.FloatField()
    marketCapitalisationPercentage = models.FloatField()
    stockExchange = models.CharField(max_length = 20, default = 'CSE')    
    def __str__(self):
        return self.companyName

class InvestmentType(models.Model):
    name = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length = 100)
    value = models.FloatField()
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name


class Investment(models.Model):
    name = models.CharField(max_length = 100)
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, default=1)
    date = models.DateTimeField(auto_now_add=True)
    investmentType = models.ForeignKey(InvestmentType)
    symbol = models.ForeignKey(ListedCompany, null = True, default = None)
    quantity = models.FloatField()
    currentValue = models.FloatField()
    
    def __str__(self):
        return self.name
       
class CompanyIssuedQuantitiesHistory(models.Model):
    quantityDifference = models.BigIntegerField()
    marketCapitalisation = models.FloatField()
    marketCapitalisationPercentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(ListedCompany)
    
class SectorIndexNames(models.Model):
    name = models.CharField(max_length = 250)
    date = models.DateTimeField(auto_now_add=True)   
    
class SectorIndex(models.Model):
    sector = models.ForeignKey(SectorIndexNames)
    price = models.FloatField();
    value = models.FloatField();
    volume = models.IntegerField();
    trades = models.IntegerField();
    date = models.DateTimeField(auto_now_add=True)    

class DailyTradeSummary(models.Model):
    company = models.ForeignKey(ListedCompany)
    shareVolume = models.BigIntegerField()
    tradeVolume = models.BigIntegerField()
    previouseClose = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    lastTradedPrice = models.FloatField()
    priceChange = models.FloatField()
    priceChangePercentage = models.FloatField()
    date = models.DateField(auto_now=True)
    turnover = models.FloatField()


class DetailedTrade(models.Model):
    company = models.ForeignKey(ListedCompany)
    shareVolume = models.BigIntegerField()
    tradeVolume = models.BigIntegerField()
    priceChange = models.FloatField()
    priceChangePercentage = models.FloatField()
    date = models.DateField(auto_now_add=True)

class CompanyFinanceReportSumary(models.Model):
    company = models.ForeignKey(ListedCompany)
    revenue = models.FloatField()
    profitBeforeTax = models.FloatField()
    profitAfterTax = models.FloatField()
    grossDividends = models.FloatField()
    interestCover = models.FloatField()
    totalAssets = models.FloatField()
    currentRatio = models.FloatField()
    issueDate = models.DateTimeField()
    description = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add=True)
    totalShareHolderFunds = models.FloatField(default=0)
    numberOfShares = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, default=1)
    PERatio = models.FloatField(default=0)
    earningsPerShare = models.FloatField(default=0)
    sharePrice = models.FloatField(default=0)
    type = models.IntegerField(default = 0)
    assetsPerShare = models.FloatField(default=0)
    devidendsPerShare = models.FloatField(default=0)
    
class Dividends(models.Model):
    investment = models.ForeignKey(Investment)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)