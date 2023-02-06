import requests, re
import subprocess
import time , numpy

most_ip = "most_ip.txt"
file2 = open(most_ip, 'w')
slow_ip = "slow_ip.txt"
file = open(slow_ip, 'w')
url = "http://bot.sudoer.net/best.cf.iran.all"
response = requests.get(url)


def give_ips():
    if response.status_code == 200:
        content = response.text
        ip_regex = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
        ips = [match.group(0) for match in ip_regex.finditer(content)]
        data = numpy.array(ips)
        counter = len(ips)
        print(f"we found {counter} IPs !")     
    else:
        print(f"Failed to retrieve data from {url} (HTTP {response.status_code})")
        
    for ip in ips:
        start = time.time()
        responsed = subprocess.run(['ping', '-c', '1','-s','65000', ip], stdout=subprocess.DEVNULL)
        end = time.time()
        most_ok = end - start < 0.4
        
        if responsed.returncode == 0 and most_ok == True:
            file2.write(f"{ip}\t is\t {most_ok} in\t {end - start:.3f}Sec\n ")
            
        else:
            print(f'{ip} is more than 0.4Sec ({end-start:.3f})')
            file.write(f'{ip} is more than 0.4Sec ({end-start:.3f})\n')
        
give_ips()