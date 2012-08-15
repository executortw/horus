try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"

import GeoIP
import os
locator = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
from datetime import datetime
from datetime import timedelta

ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'
TimeSlotLength = 1
SlotDuration = timedelta(0,0,0,0,0,TimeSlotLength)
Horusconn = sqlite3.connect(ThesisRun_PATH+'HorusDB.db')
Hcc = Horusconn.cursor()
#FindUserconn > FUconn
FUconn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Fcc = FUconn.cursor()



def FindUser(Time,Victim,AttackSource,Fcc):
    UserList = []
    TimeCov = datetime.strptime(Time,"%Y-%m-%d %H:%M:%S")
    FUQuery = Fcc.execute('SELECT DISTINCT User FROM '+AcceptTable+' WHERE Time > ? AND Time < ? AND Source = ? AND IP = ?',(Time,TimeCov+SlotDuration,Victim,AttackSource))
    UserList = list(FUQuery)
    return UserList

def FindJoint(Time,Victim,AttackSource,Fcc,UserList):
    Obflag = 0
    TimeCov = datetime.strptime(Time,"%Y-%m-%d %H:%M:%S")
    TimeCov = TimeCov + 72 * SlotDuration
    for user in UserList:
        FJQuery = Fcc.execute('SELECT Time,IP FROM '+AcceptTable+' WHERE Time > ? AND Time < ? AND Source = ? AND User = ? AND IP != ?',(Time,TimeCov,Victim,user[0],AttackSource))
	if FJQuery is None:
	    continue
	else:
	    Obflag = 5
	    FJList = list(FJQuery)
	    print 'User:',user[0]
	    for item in FJList:
		print item
    
    return Obflag

#main start from here
#First we get the Src IP list
Query = Hcc.execute('SELECT DISTINCT SrcIP FROM IPObservation ORDER BY Time ASC')
IPList = list(Query)
Observation = Hcc.execute("SELECT * FROM IPObservation WHERE DstIP != '140.117.205.1' OR DstIP != '140.117.205.10' OR DstIP != '140.117.205.5'ORDER BY Time ASC")
#Obfile = open('Obfile','w')
for Item in Observation:
#I put the column returned by Hcc into variable with meaningful name
#    print Item
    Time = Item[0]
    AttackSource = Item[1]
    Victim = Item[2]
    Scan = Item[3]
    BFA = Item[4]
    BFAS = Item[5]
    Login = Item[6]
    if Scan != 0:
	country = locator.country_name_by_addr(AttackSource)
#	Obfile.write('%s|%s|1\n'%(Time,AttackSource))
	print Time,",SEVERITY,Scanning,CATEGORY,ACTION,HITCOUNT,",AttackSource,",SRCPORT,140.117.0.0,DSTPORT"
    elif BFAS != 0:
#	Obfile.write('%s|%s|3\n'%(Time,AttackSource))
	country = locator.country_name_by_addr(AttackSource)
	#print Time, Victim, " is BFASed by ", AttackSource,"from ",country,"\033[0m"
	print Time,",SEVERITY,BFAS,CATEGORY,ACTION,HITCOUNT,",AttackSource,",SRCPORT,",Victim,",DSTPORT"
	#Because we got a BFAS(Brute Force Attack Success) here, we need to find what user account is logged in here.
	UserList = FindUser(Time,Victim,AttackSource,Fcc)
#	Obfile.write('%s|%s|%s\n'%(Time,AttackSource,FindJoint(Time,Victim,AttackSource,Fcc,UserList)))
	
    elif BFA != 0 & Login == 0:
#	Obfile.write('%s|%s|2\n'%(Time,AttackSource))
	country = locator.country_name_by_addr(AttackSource)
	print Time,",SEVERITY,BFA,CATEGORY,ACTION,HITCOUNT,",AttackSource,",SRCPORT,",Victim,",DSTPORT"
	#print Time, Victim, " is BFAed by ", AttackSource,"from ",country
    elif Login != 0 :
#	Obfile.write('%s|%s|4\n'%(Time,AttackSource))
	country = locator.country_name_by_addr(AttackSource)
#	print Time, Victim, " is Login by ", AttackSource,"from ",country


Fcc.close()
FUconn.commit()
Hcc.close()
Horusconn.commit()
"""
for IP in IPList:
    Observation = []
    print IP[0]
    Observation = Hcc.execute('SELECT * FROM IPObservation WHERE SrcIP = ? ORDER BY Time ASC',(IP[0],))
    for Item in Observation:
	print Item
"""
