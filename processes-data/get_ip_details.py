# referencia https://www.kdnuggets.com/2023/01/track-location-ip-address-python.html
from ip2geotools.databases.noncommercial import DbIpCity

def printDetails(ip):
    res = DbIpCity.get(ip, api_key="free")
    print(f"IP Address: {res.ip_address}")
    print(f"Location: {res.city}, {res.region}, {res.country}")
    print(f"Coordinates: (Lat: {res.latitude}, Lng: {res.longitude})")


ip_add = input("Enter IP: ")  
printDetails(ip_add)