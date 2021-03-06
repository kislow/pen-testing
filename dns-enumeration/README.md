# DNS Zone Transfer

Zone transfers should usually be limited to authorized slave DNS servers. Unfortunately, many administrators misconfigure their DNS servers, and as a result, anyone asking for a copy of the DNS server zone will receive one.
This is equivalent to handing a hacker the corporate network layout on a silver platter. All the names, addresses, and functionality of the servers can be exposed to prying eyes. Some DNS servers were misconfigured so badly that they did not separate their internal DNS namespace and external DNS namespace into separate, unrelated zones. This results in a complete map of the internal and external network structure.

**Note: A successful zone transfer does not directly result in a network breach. However, it does facilitate the process.** 

## <u>Getting Started</u>

Running this script on megacorpone.com (domain used by offensive-security.com) should automatically identify both name servers and attempt a zone transfer on each of them.

```sh
./dzt.sh megacorpone.com
```

## <u>Fair use</u>

Script should be used for the purpose of serving the needs of specified educational/research programs.
Do not use the acquired scripts for illegal or malicious attacks!

**Note: Similar tools exist in Kali Linux to aid DNS enumeration and most of them perform the same task.**

## <u>License</u>

This repository is published under the [MIT License](https://opensource.org/licenses/MIT).