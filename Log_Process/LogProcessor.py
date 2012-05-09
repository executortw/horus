"""
This file is to read the syslog report and find the BFA, Login message.
"""

DEBUG = 0
import sys
import LogParser
import LogDBModule

if len(sys.argv) != 3:
    print "Usage:\n\t>python LogProcessor.py <file> <source>.\nFor example:\n\t>python LogProcessor.py /var/log/241/1/1-auth.log 140.117.205.1"
else:
    filename = sys.argv[1]
    source = sys.argv[2]
    failed_logins, accept_logins = LogParser.Parser(filename,source)

    if DEBUG >= 2 :
        print "In Main:"
        print "FAILED:"
        failed_logins.sort()
        for fail in failed_logins:
            print fail
        print "++++++++++++++++++++++++++++++++++++++++++++++====================================+++++++++++++++++++++++++++++++++"
        print "ACCEPTED:"
        accept_logins.sort()
        for accept in accept_logins:
           print accept

    LogDBModule.LogintoDB(failed_logins,accept_logins,source)
