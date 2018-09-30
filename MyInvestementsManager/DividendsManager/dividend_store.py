from MyInvestementsManager.models import Dividend


def store_dividends(dividends):
    for dividend in dividends:
        existing_dividends = Dividend.objects.filter(company = dividend.company, type = dividend.type, entitled_date = dividend.entitled_date)
        if existing_dividends:
            if existing_dividends.count() > 1:
                for existing_dividend in existing_dividends:
                    print(existing_dividend)
                raise ValueError('More than one object can not exists')
            for existing_dividend in existing_dividends:
                if dividend.announced_date and ((existing_dividend.announced_date is None) or (existing_dividend.announced_date < dividend.announced_date)):
                    existing_dividend.announced_date = dividend.announced_date
                    existing_dividend.amountPerShare = dividend.amountPerShare
                    existing_dividend.payment_date = dividend.payment_date
                    existing_dividend.save()
        else:
            dividend.save()
