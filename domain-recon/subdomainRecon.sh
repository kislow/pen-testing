#!/bin/bash

# access home dir, and create recon folder
NEW_DIR=$(mkdir $(dirname "$0")/recon)

# download your index page (for educational purposes I shall use cisco)
# wget will download an index.html file into the newly created directory
TARGET_PAGE=$(wget www.cisco.com)

# testing whether directory and downloaded files are both available.
# display latest directory
VERIFY_LATEST_DIR=$(ls -td -- */ | head -n 1)
VERIFY_INDEX=$(ls index.html)

if [[ $VERIFY_LATEST_DIR != "recon/" ]] && [[ $VERIFY_INDEX != "index.html" ]];
then
    echo "directory and/or file not available"
    exit 1
fi

# get subdomain names from our TARGET_PAGE. Clean filter domains, ignore duplicates and save to new file
GET_DOMAIN_NAMES=$(sort index.html | grep -o 'http://[^"]*' | cut -d "/" -f 3 | uniq  > domainList.txt)

VERIFY_DOMAIN_LIST=`ls domainList.txt`

# extract just the IP addresses from all of this information
TARGET_IP=$(for url in $(sort ./domainList.txt); do host $url; done | grep "has address" | cut -d " " -f 4 | uniq > ipList.txt)

if [[ $VERIFY_DOMAIN_LIST != "domainList.txt" ]]
then
    echo "file not available in current directory!"
    exit 1
else
    echo $TARGET_IP && mv domainList.txt iplist.txt index.html recon/
    echo "Your recon has been successful! Find your target IPs in /recon/ipList.txt"
fi

