import os
import re
import csv
pattern = r'\(([\d.]+) ([KMGTPEZY]?B)/s\)' #thank you chatgpt

def get_download_speed(file_name):
    with open(file_name,"r") as f:
        lines = f.readlines() #get lines
        line = lines[len(lines) - 2] #get last line 
        match = re.search(pattern, line) #find the mb
        speed_number = float(match.group(1)) 
        speed_unit = match.group(2) 
        if speed_unit == "KB": #convert all to MB
            speed_number /= 1000
        #print(speed_number," MB")
    return speed_number

def main():
    with open('download.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        files = os.listdir("DownloadLogs")
        row_array = []
        for file_name in files:
            file_path = os.path.join("DownloadLogs", file_name)
            speed = get_download_speed(file_path)
            file_number = file_name[-5] #last digit in name is file number 0-9
            if file_number == "0": #first file so firstly append date and time
                row_array.append(file_name[:13])

            row_array.append(speed) #append speed

            if file_number == "9": #last file so write to csv then reset array
                writer.writerow(row_array)
                row_array = []

main()