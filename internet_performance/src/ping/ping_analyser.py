import os
import re

def save_to_csv(pings, filename = 'ping.csv'):
    ip_addresses = ["www.fmprc.gov.cn.wswebpic.com", "www.gov.scot", "www.gov.za", "www5.usp.br"]
    with open(filename, 'w') as f:
        f.write('filename,address,ip,packet_loss,rtt_min,rtt_avg,rtt_max,rtt_mdev\n')
        for file, pings in pings.items():
            for address, ping in pings.items():
                if address in ip_addresses:
                    print(address)
                    f.write(f"{file},{address},{ping['ip']},{ping['packet_loss']},{ping['rtt_min']},{ping['rtt_avg']},{ping['rtt_max']},{ping['rtt_mdev']}\n")

def process_packet_loss(line):
    # Extract the packet loss percentage
    packet_loss = re.search(r'(\d+)% packet loss', line).group(1)
    return {"packet_loss": packet_loss}

def process_rtt(line):
    # Extract the rtt values
    rtt = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', line)
    rtt_min = rtt.group(1)
    rtt_avg = rtt.group(2)
    rtt_max = rtt.group(3)
    rtt_mdev = rtt.group(4)
    return {"rtt_min": rtt_min, "rtt_avg": rtt_avg, "rtt_max": rtt_max, "rtt_mdev": rtt_mdev}

def process_log_contents(contents):
    pings = {}
    current_log = {}
    for line in contents.split('\n'):
        # Ignore if line is empty
        if line == '':
            continue
        
        # If line is a PING line
        if 'PING' in line:
            if current_log:
                pings[current_log['address']] = current_log
                current_log = {}
            
            lines = line.split(' ')
            current_log['address'] = lines[1]
            current_log["ip"] = re.sub(r'[()]', '', lines[2])
            
        # If line is a ping result line
        elif 'packets transmitted' in line:
            current_log.update(process_packet_loss(line))
            
        # If line is a rtt line
        elif 'rtt' in line:
            current_log.update(process_rtt(line))
            
    pings[current_log['address']] = current_log
            
    return pings

def loop_through_files(folder = 'PingLogs'):
    output = {}
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            with open(os.path.join(folder, file), 'r') as f:
                contents = f.read()
                pings = process_log_contents(contents)
                output[file] = pings
    return output

if __name__ == '__main__':
    pings = loop_through_files()
    save_to_csv(pings)
