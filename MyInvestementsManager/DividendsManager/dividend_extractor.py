import datetime
import json
import re

from MyInvestementsManager.models import ListedCompany, DividendType, Dividend
from MyInvestementsManager.util.ApplicationConstants import URL_CSE
from MyInvestementsManager.util.HTTPModule.HttpInterface import getDataByHttpsWithBody


def read_latest_dividends(symbol):
    dividends = []

    foo = {'symbol': str(symbol)}
    all_announcements = getDataByHttpsWithBody('https://' + URL_CSE + '/api/announcements', foo)

    if all_announcements:
        dividends_for_company = filter_dividends(all_announcements, symbol)
        if dividends_for_company:
            dividends.extend(dividends_for_company)

    return dividends


def filter_dividends(announcements, symbol):
    json_data = json.loads(announcements)

    company = ListedCompany.objects.get(symbol=symbol)

    dividends = []
    for announcement in json_data['infoAnnouncement']:
        title = announcement['title']
        if title:
            title = title.replace(' ', '').upper()
            # Try with the body
            body = announcement['body']
            if title == 'DIVIDENDANNOUNCEMENT' or title == 'DIVIDENDANNOUNCEMENTS' or title == 'DIVIDENDANNOUNCEMENT(AMENDED)' or title == 'DIVIDENDANNOUNCEMENTS(INTERIMANDFINAL)' or title in 'DIVIDENDANNOUNCEMENT' or title in 'DIVIDENDANNOUNCEMENT(DATES)':
                dividend = create_dividends(body, company)
                if dividend:
                    dividends.extend(dividend)
            elif title == "SCRIPDIVIDEND" or title == 'CASHANDSCRIPDIVIDEND' or title == 'CASH&SCRIPDIVIDEND' or title == 'CASH&SCRIPDIVIDENDANNOUNCEMENT' or title == 'CASH&SCRIPDIVIDENDS' or title == 'DIVIDENDANNOUNCEMENTS(CASH&SCRIP)' or title == 'CASHANDSCRIPDIVIDENDANNOUNCEMENT' or (
                    "DIVIDEND" in title and "RIGHTSISSUE" in title):
                dividend = create_dividends(body, company)
                if dividend:
                    dividends.extend(dividend)
            elif 'EMPLOYEESHAREOPTIONSCHEME' in title or 'GENERALMEETING' in title or 'CHANGEINDIRECTORATE' in title or title == 'EMPLOYEESHAREOPTIONSCHEME' or title == 'EMPLOYEESHAREOPTIONSHCEME' or title == 'DEALINGSBYDIRECTORS' \
                    or 'DISCLOSURE' in title or 'NOTIFICATIONONTHELISTINGSOFSHARES' in title or 'WARRANT' in title or 'PRESSRELEASE' in title or title == 'EMPLOYEESHAREOPTIONPLAN' or title == 'SUBDIVISIONOFSHARES' or 'GeneralMeeting' in title \
                    or title == 'RATINGREVIEW' or 'RIGHTSISSUE' in title or title == 'ANNOUNCEMENT' or 'PURCHASEOFSHARES' in title or 'CHANGEOFREGISTEREDOFFICE' == title or 'FITCH' in title or 'CLARIFICATION' in title or 'Disclosure' in title or 'RETIREMENT' in title \
                    or 'CHANGEOF' in title or 'FINANCIALSTATEMENT' in title or 'CHAIRMAN' in title or 'Financial' in title or 'TRANSACTION' in title or 'CIRCULAR' in title or 'DEBENTURE' in title or 'NOTIFICATION' in title or 'DATES' in title or 'DISLCOSURE' in title \
                    or 'Halted' in title or 'SUBSIDIARY' in title or 'SUMMARY':
                pass
            else:
                raise ValueError("Undefined Dividend Type: " + title)

    return dividends


# def parse_date(date):
# return datetime.datetime.strptime(summary['issueDate'], "%d/%b/%Y").date()


def create_dividends(body, company):
    if (body):
        contents = body.encode("utf-8").split("\r<br>")

        amount = None
        announced_date = None
        entitled_date = None
        payment_date = None
        scripDividendPerShare = None

        terminate = False

        for content in contents:
            if content:
                key_val = []
                content = content.replace(' ', '').upper()
                if content.upper().startswith('DATESTOBENOTIFIED'):
                    terminate = True
                    break
                elif ':-' in content:
                    key_val = content.split(':-')
                elif ":" in content:
                    key_val = content.split(':')
                elif content.startswith("DATEOFANNOUNCEMENT."):
                    key_val.append('DATEOFANNOUNCEMENT')
                    key_val.append(content.split('DATEOFANNOUNCEMENT.')[1])
                elif content.startswith('RATEOFDIVIDEND'):
                    key_val.append('RATEOFDIVIDEND')
                    key_val.append(re.findall('\d+.\d+', content)[0])
                elif '-' in content:
                    key_val = content.split('-')
                else:
                    continue

                key = key_val[0]
                val = key_val[1]

                if 'DATEOFANNOUNCEMENT' == key or 'DATEANNOUNCEMENT' == key or 'DATEOFINITIALANNOUNCEMENT' == key:
                    announced_date = parse_date(val)
                elif 'XD' == key:
                    entitled_date = parse_date(val)
                elif 'PAYMENT' == key:
                    payment_date = parse_date(val)
                elif 'RATEOFDIVIDEND' == key or 'DIVIDENDPERSHARE' == key:
                    val = val.replace('(LessWHT)', '')

                    if 'PERSHARE' in val:
                        val = val.split('PERSHARE')[0]

                    result = re.findall('\d+\.\d+', val)
                    if len(result) == 0:
                        regx = re.compile('CENTS\d+')
                        if regx.search(val):
                            result = re.findall('\d+', val)
                            amount = float(result[0]) / 100

                    if not amount:
                        amount = float(result[0])

                elif 'PROPORTION' == key:
                    scripDividendPerShare = get_amount_from_propotion(val)
                elif 'AGM' == key and 'TOBENOTIFIED' in val.upper():
                    terminate = True
                    break

        dividends = []

        if entitled_date:
            # cash dividend
            if amount:
                dividend_type = DividendType.objects.get(name='CASH')
                dividend = Dividend(type=dividend_type, company=company, amountPerShare=amount,
                                    announced_date=announced_date, entitled_date=entitled_date,
                                    payment_date=payment_date)
                dividends.append(dividend)
            # Scrip Dividend
            if scripDividendPerShare:
                dividend_type = DividendType.objects.get(name='SCRIP')
                dividend = Dividend(type=dividend_type, company=company, amountPerShare=scripDividendPerShare,
                                    announced_date=announced_date, entitled_date=entitled_date,
                                    payment_date=payment_date)
                dividends.append(dividend)
            if not dividends:
                raise ValueError("At least one Dividend should exist for " + body)
        elif terminate:
            return
        else:
            raise ValueError("Dividend does not have all the necessary values for " + body)
        return dividends


def parse_date(date_str):
    date_str = date_str.replace('ARP', 'APR')
    date_str = date_str.replace('TH', '')
    try:
        return datetime.datetime.strptime(date_str, "%d.%b.%Y").date()
    except Exception:
        try:
            return datetime.datetime.strptime(date_str, "%d.%B.%Y").date()
        except Exception:
            try:
                return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
            except Exception:
                return datetime.datetime.strptime(date_str, "%d.%b%Y").date()


def get_amount_from_propotion(propotion):
    # check the type using a regxp
    # if matches to a certain type, parse using that type
    # define all the accepted types in a constant array
    propotion = propotion.upper()
    dataToProcess = None
    if '/' in propotion:
        shareTypes = propotion.split('/')
        for data in shareTypes:
            if 'NON-VOTING' not in data:
                dataToProcess = data
                break
    else:
        dataToProcess = propotion

    if 'VOTING' in dataToProcess:
        data = dataToProcess.split('VOTING')[1]
    else:
        data = dataToProcess

    if ('FOR' in data):
        propotion = data.split('FOR')
        numberOfShares = extract_number(propotion[0])
        perShares = extract_number(propotion[1])

        if (numberOfShares > 0 and perShares > 0):
            return perShares / numberOfShares

    raise ValueError("Could not extract the Scrip Dividend proportions for : " + propotion)


def extract_number(str):
    return float(re.findall("\d+\.\d+|\d+", str)[0])
