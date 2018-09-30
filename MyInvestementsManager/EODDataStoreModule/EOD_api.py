from MyInvestementsManager.models import DailyTradeSummary


def getLastTradedPrice(company):
    summary = DailyTradeSummary.objects.filter(company=company).order_by('-date').first()
    if summary:
        return summary.lastTradedPrice
    else:
        return None