#!/usr/bin/python3

import time, sys, os, random, psutil as ps, subprocess as sp, netifaces as nif

# define max limit of bandwidth in bytes
define_bandwidth_limit = 200000

# stops bandwidth consumption before max define_bandwidth_limit has been reached
bandwidth_consumption_limit = define_bandwidth_limit - (define_bandwidth_limit / 4 )

def calculate_bandwidth_consumption():

    def convert_to_mbit(value):
        value = float(value)
        KB = float(1024)
        MB = float(KB ** 2)

        return '{0:.2f} MB'.format(value/MB)

    # print the total consumed bandwidth in MB
    def send_stat(value):
        print('Total Data consumed:' + str(convert_to_mbit(value)))

    def limit_consumption(consumed):
        print('LIMIT REACHED: ' + str(convert_to_mbit(consumed)) + ' consumed!')

    starting_value = 0

    # use byte_counter_reset variable to show consumption starting at value 0
    byte_counter_reset = ps.net_io_counters().bytes_sent + ps.net_io_counters().bytes_recv

    while True:
        usage = ps.net_io_counters().bytes_sent + ps.net_io_counters().bytes_recv

        if starting_value:
            send_stat(usage - byte_counter_reset)

        starting_value = usage

        time.sleep(1)

        # calculate the consumed bandwidth
        consumed_bandwidth = starting_value - byte_counter_reset

        if consumed_bandwidth > bandwidth_consumption_limit:
            return limit_consumption(consumed_bandwidth)
            break

#----------------function to reset network and spoof mac address (root user required)-------------------#

def generate_mac():
    mac_address = [  0x90, 0x09, 0x20,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]

    random_mac_address = ':'.join(map(lambda x: "%02x" % x, mac_address))
    print("Successfully generated a new mac address: " + random_mac_address)

def spoof_mac_address():

    network_interface = nif.gateways()
    default_network_interface = network_interface['default'][nif.AF_INET][1]

    network_interface = os.environ["NETINT"] = str(default_network_interface)
    os.environ.get('NETINT')

    # Retrieve mac address of default network interface
    p1 = sp.Popen(['ip', 'link', 'show', network_interface], stdout=sp.PIPE)
    p2 = sp.Popen(["awk", "/ether/ {print $2}"], stdin=p1.stdout, stdout=sp.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = p2.communicate()[0]

    print('WARNING: Only root user can modify the mac address!')

    new_mac = generate_mac()

    os.environ["MAC"] = str(new_mac)
    export_mac_address = os.environ.get('MAC')

    if (output == new_mac):
        print("MAC addresses are identical, closing application...")
        sys.exit(1)
    else:
        sp.run(['sudo ip link set dev $NETINT down'], shell=True)
        sp.run(['sudo ip link set dev $NETINT address $MAC'], shell=True)
        sp.run(['sudo ip link set dev $NETINT up'], shell=True)
        print('Applying changes...')
        time.sleep(2)
        print('The new mac address has been applied to your default network interface...')


if __name__ == "__main__":
    calculate_bandwidth_consumption()
    spoof_mac_address()
