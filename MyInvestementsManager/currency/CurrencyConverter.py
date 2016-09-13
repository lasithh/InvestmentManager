from MyInvestementsManager.models import Currency
from MyInvestementsManager.util.ApplicationConstants import DEFAULT_CURRENCY

def valueInDefaultCurrency (investmentInFromCurrency):
    
    defaultCurrency = Currency.objects.get(name = DEFAULT_CURRENCY)
    
    sourceCurrency = investmentInFromCurrency.currency
    
    investmentInFromCurrency.amount *= sourceCurrency.value
    investmentInFromCurrency.currency = defaultCurrency
    investmentInFromCurrency.currentValue *= sourceCurrency.value
    
    return investmentInFromCurrency