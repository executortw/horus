"""
This file is to read the syslog report and find the BFA, Login message.
"""


import sys
import LogParser

if len(sys.argv) != 2:
    print "Usage:\n\t>python LogProcessor.py <path>.\nFor example:\n\t>python LogProcessor.py /var/log/241/1/1-auth.log"
else:
    filename = sys.argv[1]
    LogParser.Parser(filename)
