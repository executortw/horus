"""
In this file, we parse the text in the file to count and verify the BFA and login phenomenal.
"""

DEBUG = 0
from logsparser.lognormalizer import LogNormalizer as LN
import GeoIP
import re

normalizer = LN('/usr/share/logsparser/normalizers')
locator = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)



def Parser(filename,source):#source specify the localhost we are processing
    auth_logs = open(filename,'r')
    failed_logins = []
    failed_login = []
    accept_logins = []
    accept_login = []
    for log in auth_logs:
	l = {"raw":log}
        normalizer.normalize(l)
	if DEBUG >= 3:
            print "RAW:", log 
	try:
            if l.get('action') == 'fail':
		failed_login = [l.get('date'),l.get('source_ip'),l.get('user')]
		if DEBUG >= 3:
		    print "Failed:" , failed_login
		failed_logins.append(failed_login)
            elif l.get('action') == 'accept':
	        accept_login = [l.get('date'),l.get('source_ip'),l.get('user')]
		if DEBUG >= 3:
		    print "Successful login: ", accept_login
		accept_logins.append(accept_login)
	
	except:
	    print "Exception!"
	    print "Excepted RAW:",log
	    print "Excepted process:", accept_login

	    
    if DEBUG >= 2 :
        print "FAILED:"
    	failed_logins.sort()
	for fail in failed_logins:
	    print fail
        print "++++++++++++++++++++++++++++++++++++++++++++++====================================+++++++++++++++++++++++++++++++++"
        print "ACCEPTED:" 
	accept_logins.sort()
        for accept in accept_logins:
	   print accept

    return (failed_logins, accept_logins)


