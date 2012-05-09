"""
In this file, we parse the text in the file to count and verify the BFA and login phenomenal.
"""

DEBUG = 0
from logsparser.lognormalizer import LogNormalizer as LN
import GeoIP
import re

normalizer = LN('/usr/share/logsparser/normalizers')
locator = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

def Parser(filename):
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
	        country = locator.country_name_by_addr(l['source_ip'])
	        if country:
		    #IF GeoIP could identify where the login comes from
                    failed_login = [l.get('date'),l.get('source'),l.get('source_ip'),country,l.get('user')]
		    if DEBUG >= 3:
			print "Failed with country located:" , failed_login
	            failed_logins.append(failed_login)
                else:
	            #If GeoIP couldn't identify where the login comes from
	            failed_login = [l.get('date'),l.get('source'),l.get('source_ip'),"Unknown",l.get('user')]
		    if DEBUG >= 3:
			print "Failed with no country:", failed_login
		    failed_logins.append(failed_login)
            elif l.get('action') == 'accept':
	        country = locator.country_name_by_addr(l['source_ip'])
	        if country:
                #IF GeoIP could identify where the login comes from
	            accept_login = [l.get('date'),l.get('source'),l.get('source_ip'),country,l.get('user')]
		    if DEBUG >= 3:
			print "Successful login with country located:", accept_login
		    accept_logins.append(accept_login)
                else:
	            #If GeoIP couldn't identify where the login comes from
	            accept_login = [l.get('date'),l.get('source'),l.get('source_ip'),"Unknown",l.get('user')]
		    if DEBUG >= 3:
			print "Successful login without country located:", accept_login
		    accept_logins.append(accept_login)
	
	except:
	    print "Exception!"
	    print "Excepted RAW:",log
	    print "Excepted process:", accept_login

    print "FAILED:",failed_logins
    print "++++++++++++++++++++++++++++++++++++++++++++++====================================+++++++++++++++++++++++++++++++++"

    print "ACCEPTED:", accept_logins
    print type(failed_logins[0][0])
