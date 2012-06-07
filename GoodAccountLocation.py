try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"
import os
import GeoIP
import urllib
locator = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)



ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'
Horusconn = sqlite3.connect(ThesisRun_PATH+'HorusDB.db')
Hcc = Horusconn.cursor()
#FindUserconn > FUconn
FUconn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Fcc = FUconn.cursor()




AccountList = list(Fcc.execute('SELECT DISTINCT User FROM '+AcceptTable))
for i in range(len(AccountList)):
    ID = AccountList[i][0]
    print "ID:",ID
    GoodManSource = Fcc.execute('SELECT DISTINCT IP FROM AcceptRecord WHERE User = ?',(ID,))
    for eachIP in GoodManSource:
	country = locator.country_name_by_addr(eachIP[0])
	"""
	if country == None:
	    response = urllib.urlopen('http://api.hostip.info/get_html.php?ip='+eachIP[0]+'&position=true').read()
	    print "IP:",eachIP,"HOSTIP Country:",response
	else:
	    print "IP:",eachIP,"GeoIP ans-Country:",country
	"""
	print "IP:",eachIP,"GeoIP ans-Country:",country
