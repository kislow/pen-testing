#!/usr/bin/python3

# import required python modules
import time, sys, os, random, psutil as ps, subprocess as sp, netifaces as nif

# (Gloabl) variable to define max limit of bandwidth consumption
bandwidth_limit = 200000

# (Global) variable smart limit stops bandwidth consumption before max bandwidth_limit has been reached
smart_limit = bandwidth_limit - (bandwidth_limit / 4 ) 


# Bandwidth consumption logic
def bandwidth_consumption_calculator():
    
     # function to convert total psutil bytes to  KB & MB 
    def convert_to_mbit(value):
        value = float(value)
        KB = float(1024)
        MB = float(KB ** 2)

        return '{0:.2f} MB'.format(value/MB)

    # print the total consumed bandwidth in MegaByte format
    def send_stat(value):
        print('Total Data consumed:' + str(convert_to_mbit(value)))

    # limit bandwidth consumption
    def consumption_limit(consumed):
        print('LIMIT REACHED: ' + str(convert_to_mbit(consumed)) + ' consumed!')
    
    # start counting from 0
    starting_value = 0    
    # use byte_counter_reset variable to show consumption starting at value 0  
    byte_counter_reset = ps.net_io_counters().bytes_sent + ps.net_io_counters().bytes_recv   
    
    # loop over consumed bandwdith until limit reached
    while True:
        usage = ps.net_io_counters().bytes_sent + ps.net_io_counters().bytes_recv

        if starting_value:
            send_stat(usage - byte_counter_reset)
        
        starting_value = usage
        
        # delay printing consumption for x seconds
        time.sleep(1)

        # calculate the consumed bandwidth
        consumed_bandwidth = starting_value - byte_counter_reset 

        if consumed_bandwidth > smart_limit:
            return consumption_limit(consumed_bandwidth)
            break
        
#----------------function to reset network and spoof mac address (root user required)-------------------#

def generate_mac_address():
      # get default network interface
    find_interfaces = nif.gateways()
    default_interface = find_interfaces['default'][nif.AF_INET][1]
    
    # # setting shell environment variable necessary because if interface is shut, default_interface can no longer be found by python 
    network_interface = os.environ["NETINT"] = str(default_interface)
    os.environ.get('NETINT')
    
    # Retrieve mac address of default network interface 
    p1 = sp.Popen(['ip', 'link', 'show', network_interface], stdout=sp.PIPE)
    p2 = sp.Popen(["awk", "/ether/ {print $2}"], stdin=p1.stdout, stdout=sp.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]

# Generate random mac address
    mac = [  0x90, 0x09, 0x20,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    new_random_mac = ':'.join(map(lambda x: "%02x" % x, mac))
    print("Successfully generated a new mac address: " + new_random_mac)
    
    print('WARNING: Only root user can modify the mac address!')
    
    #set shell environment variable for the generated mac address
    os.environ["MAC"] = str(new_random_mac)
    export_mac_address = os.environ.get('MAC')
        
    if (output == new_random_mac):
        print("MAC addresses are identical, closing application...")
        sys.exit(1)
    else:
        # temporarily disable interface to avoid error message
        sp.run(['sudo ip link set dev $NETINT down'], shell=True)
        # spoof your mac address
        sp.run(['sudo ip link set dev $NETINT address $MAC'], shell=True)
        # enable interface
        sp.run(['sudo ip link set dev $NETINT up'], shell=True)
        print('Applying changes...')
        time.sleep(2)
        print('The new mac address has been applied to your default network interface...')
        
# invoke functions 
if __name__ == "__main__":
    bandwidth_consumption_calculator()
    generate_mac_address()