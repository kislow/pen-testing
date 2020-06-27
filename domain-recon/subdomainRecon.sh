#!/bin/bash

# access home dir, and create recon folder
newDir=`mkdir $(dirname "$0")/recon`

# download your index page (for educational purposes I shall use cisco)
# wget will download an index.html file into the newly created directory
targetPage=`wget www.cisco.com`

# testing whether directory and downloaded files are both available.
# display latest directory
verifyLatestDir=`ls -td -- */ | head -n 1`
verifyIndex=`ls index.html`

if [[ $verifyLatestDir != "recon/" ]] && [[ $verifyIndex != "index.html" ]];
then
    echo "directory and/or file not available"
    exit 1
fi

# get subdomain names from our targetPage. Clean filter domains, ignore duplicates and save to new file
getDomainNames=`sort index.html | grep -o 'http://[^"]*' | cut -d "/" -f 3 | uniq  > domainList.txt`

verifyDomainList=`ls domainList.txt`

# extract just the IP addresses from all of this information
targetIP=`for url in $(sort ./domainList.txt); do host $url; done | grep "has address" | cut -d " " -f 4 | uniq > ipList.txt`

if [[ $verifyDomainList != "domainList.txt" ]]
then
    echo "file not available in current directory!"
    exit 1
else
    echo `$targetIP && mv domainList.txt iplist.txt index.html recon/` 
    echo "Your recon has been successful! Find your target IPs in /recon/ipList.txt"
fi

