# Snorkel script

There are still many infrastructures that use mac-filters to restrict/limit network access.
A security researcher may use this snorkel script to test a network bandwidth limitation.

## Prerequisites

```html
Linux OS with root user permission required.
Python script has been written and tested on a linux OS.
```

## Requirements

```python
Python version > 3.2 required!
```

The following python modules are used/required:

- time
- sys
- os
- random
- psutil
- subprocess
- netifaces

## Getting Started

After cloning the project, open the python file in your preferred editor and set bandwidth_limit in bytes:

```python
bandwidth_limit = 200000
```

(E.g. 200000 bytes is roughly equal to 0.2MB in our test scenario)

Save script after setting the bandwidth_limit and execute script in a terminal:

```sh
./snorkel.py
```

The script will stdout the amount of bandwidth consumed in intervals of a second.
Afterwards, it will spoof the mac address of your default network interface.
Once bandwidth limit has been reached and network mac address has been spoofed, try to reconnect to the network.
If you can successfully connect to the network and get recognised as a new client, the script has accomplished its purpose.

## Fair use

Script should be used for the purpose of serving the needs of specified educational/research programs.

Do not use the acquired scripts for illegal or malicious attacks!

## License

This repository is published under the [MIT License](https://opensource.org/licenses/MIT).
