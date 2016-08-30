from django.db import models

# Create your models here.
class Investment(models.Model):
    name = models.CharField(max_length = 100)
    amount = models.IntegerField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.name
    
class ListedCompany(models.Model):
    companyName = models.CharField(max_length = 250)
    symbol = models.CharField(max_length = 20)
    price = models.FloatField()
    issuedQuentity = models.BigIntegerField()
    marketCapitalisation = models.FloatField()
    marketCapitalisationPercentage = models.FloatField()
    
    def __str__(self):
        return self.companyName
    
class CompanyIssuedQuantitiesHistory(models.Model):
    quantityDifference = models.BigIntegerField()
    marketCapitalisation = models.FloatField()
    marketCapitalisationPercentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(ListedCompany)
    
class MarketIndex(models.Model):
    sector = models.CharField(max_length = 250)
    price = models.FloatField();
    value = models.FloatField();
    volume = models.IntegerField();
    trades = models.IntegerField();
    
class MarketIndexHistory(models.Model):
    sector = models.CharField(max_length = 250)
    price = models.FloatField();
    value = models.FloatField();
    volume = models.IntegerField();
    trades = models.IntegerField();
    date = models.DateTimeField();
    

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
    date = models.DateField()
    turnover = models.FloatField()


class DetailedTrade(models.Model):
    company = models.ForeignKey(ListedCompany)
    shareVolume = models.BigIntegerField()
    tradeVolume = models.BigIntegerField()
    priceChange = models.FloatField()
    priceChangePercentage = models.FloatField()
    date = models.DateField()
