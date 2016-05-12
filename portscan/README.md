portScan
========

Simple port scan script in Python. Work is still in progress.
portScan.py requires Python3 while scapyScan.py requires Python2.x. I'm working on writing both in same version.

For Scapy scans using scapyScan.py script:

Usage: scapyScan.py [options]

Options:
  -h, --help            show this help message and exit
  -t target.com, --target=target.com
  -p PORTS, --ports=PORTS  Ports separated by commas and no spaces.
  -s [timeout in seconds], --timeout=[timeout in seconds]
  -S (c) TCP Connect, TCP (s) Stealth, (x)XMAS, or (f) FIN scan., --scantype=(c) TCP Connect, TCP (s) Stealth, (x)XMAS, or (f) FIN scan.
  
  More features coming soon
