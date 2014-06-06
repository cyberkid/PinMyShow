import pyipinfodb
from config import Config


def getIPInfo(ip):
    ip_lookup = pyipinfodb.IPInfo(Config.API_KEY_IPINFODB)
    res = ip_lookup.get_country(ip)
    return res['countryCode']
