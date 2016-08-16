import json
import urllib3
import certifi

urlbase = "http://theastrologer-api.herokuapp.com/api/horoscope/{0}/{1}"
http = urllib3.PoolManager(cert_reqs = 'CERT_REQUIRED', ca_certs = certifi.where())

def getJson(url):
    r = http.request('GET', url)
    return json.loads(r.data.decode('utf-8'))

def getToday(s):
    horoscope = getJson(urlbase.format(s.lower(), "today"))

    returnHoro = (
        "```\n" +
        "Horoscope for {0} on {1}.\n\n".format(s.title(), horoscope['date']) +
        "{0}\n".format(horoscope['horoscope']) +
        "```"

    )

    return returnHoro
