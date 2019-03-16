from MyInvestementsManager.models import DailyTradeSummary


def getLastTradedPrice(company):
    summary = DailyTradeSummary.objects.filter(company=company).order_by('-date').first()

    if summary:
        if summary.lastTradedPrice > 0.0:
            return summary.lastTradedPrice
        else:
            return summary.previouseClose
    else:
        return None