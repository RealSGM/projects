import pandas as pd
import math
import geoip2.database

folder = 'TraceRouteCode'
reader_asn = geoip2.database.Reader(folder+'/GeoLite2-ASN.mmdb')
reader_city = geoip2.database.Reader(folder+'/GeoLite2-City.mmdb')
ip_lookup = {}

ip_addresses = {
    "www.fmprc.gov.cn":{"Time": [], "Distance": []}, 
    "www.gov.scot":{"Time": [], "Distance": []}, 
    "www.gov.za":{"Time": [], "Distance": []}, 
    "www5.usp.br":{"Time": [], "Distance": []}
}

def get_coordinates(ip_address):
    longitude = None
    latitude = None
    location = None
    
    try:
        response = reader_city.city(ip_address)
        
        ## Check if response has a location attribute
        if response.location.latitude is None or response.location.longitude is None:
            return longitude, latitude, location
        
        longitude = response.location.longitude
        latitude = response.location.latitude
        location = response.city.name
        ip_lookup[ip_address] = (latitude, longitude, location)
        
        
    except geoip2.errors.AddressNotFoundError:
        pass
    return latitude, longitude, location

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    r = 6371  # Radius of Earth in kilometers
    distance = r * c
    return distance

def check_coord_valid(coord): 
    if coord is None:
        return False
    if coord[0] is None:
        return False
    if coord[1] is None:
        return False
    return True

def load_csv(path):
    return pd.read_csv(path)

def main(path):
    traceroute_results = load_csv(path)
    
    for (file, address), group in traceroute_results.groupby(['File', 'Address']):
        total_time = 0
        total_distance = 0
        previous_distance = None
        
        for i, row in group.iterrows():
            ## Add the time to the total time
            total_time += row['Average Time']

            ## Calculate distance
            ip = row['IP']
            latitude, longitude, location = get_coordinates(ip)
            
            if check_coord_valid(previous_distance) & check_coord_valid((latitude, longitude)):
                distance = haversine(previous_distance[0], previous_distance[1], latitude, longitude)
                total_distance += distance
                
            previous_distance = (latitude, longitude)
            
        ip_addresses[address]["Time"].append(total_time)
        ip_addresses[address]["Distance"].append(total_distance)
    
    for address in ip_addresses:
        print(address)
        print(round(sum(ip_addresses[address]["Time"])/len(ip_addresses[address]["Time"]),2))
        print(round(sum(ip_addresses[address]["Distance"])/len(ip_addresses[address]["Distance"]),2))
        print("-"*10)

main('TraceRouteCode/traceroute.csv')