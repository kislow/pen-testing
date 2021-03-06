#!/usr/local/bin/python3

import os, platform, sys
from datetime import datetime 

# Request user input
net = input("Enter the Network Address: ")
net1 = net.split('.')

a = '.'
#concatenate ip address
net2 = net1[0] + a + net1[1] + a + net1[2] + a

# request user input (4th Octect)
starting_value = int(input("Enter the Starting Number: "))
last_value = int(input("Enter the Last Number: "))
last_value = last_value + 1

# create platform-independent ping sweep
operating_system = platform.system()

if (operating_system == "Windows"):
    ping1 = "ping -n 1 "
elif (operating_system == "Linux"):
    ping1 = "ping -c 1 "
else: 
    ping1 = "ping -c 1 "

t1 = datetime.now()
print("Scanning in Progress...")

for ip in range(starting_value, last_value):
    address = net2 + str(ip)
    cmd = ping1 + address
    response = os.popen(cmd)
    
    # loop over a ttl exisitence check 
    for line in response.readlines():
        if ('ttl' not in line.lower()):
            continue
        if ('ttl' in line.lower()):
            print(address, "--> Live")

t2 = datetime.now()
total = t2 - t1

print("Scanning complete in: ", total)
    