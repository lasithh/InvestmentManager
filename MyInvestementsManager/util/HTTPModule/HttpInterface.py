import httplib
import shutil
import urllib
import urllib2
import requests


def getDataByHttps(domainUrl, path, method='POST'):
    conn = httplib.HTTPSConnection(domainUrl)
    conn.request(method, path)
    r = conn.getresponse()
    s = r.read().decode('utf-8')
    return s


def getDataByHttpsWithBody(url, values):
    body = urllib.urlencode(values)
    req = urllib2.Request(url, body)
    response = urllib2.urlopen(req)
    return response.read().decode('utf-8')


def download_file(url, file_path):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    with open(file_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)