import pandas as pd
import geoip2.database
import folium

folder = 'TraceRouteCode'

# save_folder = folder+'/Maps'
# path = folder+'/traceroute.csv'
path = folder+'/russia.csv'
save_folder = folder+'/Russia'

reader_asn = geoip2.database.Reader(folder+'/GeoLite2-ASN.mmdb')
reader_city = geoip2.database.Reader(folder+'/GeoLite2-City.mmdb')


ip_addresses = {
    "www.fmprc.gov.cn": {}, 
    "www.gov.scot": {}, 
    "www.gov.za": {}, 
    "www5.usp.br": {},
    "point.mephi.ru": {}
}


ip_lookup = {}

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

def load_csv(path):
    return pd.read_csv(path)

def main(path):
    traceroute_results = load_csv(path)
    
    # Loop through traceroute results, and separate the rows by File and Address
    for (file, address), group in traceroute_results.groupby(['File', 'Address']):
        
        m = folium.Map(location=[0, 0], zoom_start=2)
        coordinates = []
        
        # Iterate over the rows in the group
        for i, row in group.iterrows():
            
            # Get the coordinates of the IP address
            latitude, longitude, location = ip_lookup.get(row['IP'], get_coordinates(row['IP']))
                
            if longitude is not None and latitude is not None:
                folium.CircleMarker(
                    [latitude, longitude], 
                    popup = location,
                    radius = 1,
                    fill = True,
                    color = "black",
                    fill_color = "red",
                ).add_to(m)
                
                coordinates.append([latitude, longitude])
                
        # Add lines between markers
        folium.PolyLine(coordinates, color="red", weight=2.5, opacity=1).add_to(m)
                
        # address = address.split('.')[1]
        file_name = f'{address}_{file}.html'
        m.save(f'{save_folder}/{file_name}')
        
        

if __name__ == '__main__':
    main(path)