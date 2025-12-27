import os
import re
import csv

ip_addresses = {"www.fmprc.gov.cn": [], "www.gov.scot": [], "www.gov.za": [], "www5.usp.br": [], "point.mephi.ru": []}
output = {}
ip_pattern = r'([\d]+\.[\d]+\.[\d]+\.[\d]+|\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b)'

def extract_url_from_traceroute(log_line):
    # Regular expression pattern to match the URL
    pattern = r'traceroute to ([\w.-]+)'
    match = re.search(pattern, log_line)
    if match:
        return match.group(1)
    else:
        return None
    
def remove_duplicates(cleaned_lines):
    ip_count = 0
    filtered_list = []
    
    for item in cleaned_lines:
        if re.match(ip_pattern, item):
            ip_count += 1
        if ip_count <= 1:
            filtered_list.append(item)    
    return filtered_list

def calculate_average_time(cleaned_lines):
    total_time = 0
    count = 0
    for item in cleaned_lines[3:]:
        total_time += float(item)
        count += 1
    return round(total_time / count, 2)

def process_line(line):
    cleaned_lines = line.split(' ')
    cleaned_lines = [item for item in cleaned_lines if item != 'ms'] # remove ms
    cleaned_lines = [item for item in cleaned_lines if '*' not in item] # remove *
    cleaned_lines = list(filter(None, cleaned_lines)) # remove empty strings
    cleaned_lines = remove_duplicates(cleaned_lines)
            
    hop_dict = {}
    hop_dict['hop'] = cleaned_lines[0]
    hop_dict['address'] = cleaned_lines[1]
    hop_dict['ip'] = re.sub(r'[()]', '', cleaned_lines[2])
    hop_dict['average_time'] = calculate_average_time(cleaned_lines)
    
    return hop_dict

def process_log_contents(contents):
    # Dictionary to store the hops
    hops = {}
    current_hop = None
    
    # Loop through each line in the contents
    for line in contents.split('\n'):
        # Extract the URL from the traceroute line
        match = re.search(ip_pattern, line)
        if match:
            hop = match.group(0)

            if 'traceroute' in line:
                current_hop = str(hop)
                if current_hop not in hops:
                    hops[current_hop] = []
            else:
                hop_dict = process_line(line)
                
                hops[current_hop].append(hop_dict)
    return hops

def loop_through_files(folder='TraceRouteLogs'):
    # Loop through all the files in the folder
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            # Open the file and read its contents
            with open(os.path.join(folder, file), 'r') as f:
                contents = f.read()
                hops = process_log_contents(contents)
                output[file] = hops

def save_to_csv(output, filename='traceroute.csv'):
    with open('TraceRouteCode/' + filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File', 'Address', 'Hop', 'IP', 'Average Time'])
        for file, hops in output.items():
            for address, hop_list in hops.items():
                for hop in hop_list:
                    if address in ip_addresses.keys():
                        writer.writerow([file, address, hop['hop'], hop['ip'], hop['average_time']])

def file_server_route_checker():
    with open('TraceRouteCode/file_server_route.txt', 'r') as f:
        contents = f.read()
        hops = process_log_contents(contents)
        output['point.mephi.ru'] = hops
        save_to_csv(output, 'point.mephi.ru.csv')

if __name__ == '__main__':
    file_server_route_checker()
#     loop_through_files()
#     save_to_csv(output)

