import pyipinfodb
from config import Config

def getIPInfo(ip):
    ip_lookup = pyipinfodb.IPInfo(Config.API_KEY_IPINFODB)
    return ip_lookup.get_country(ip)
