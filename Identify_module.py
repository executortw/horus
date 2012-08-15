"""
"""

try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"
from datetime import datetime
from datetime import timedelta
import os
TimeSlotLength = 1
SlotDuration = timedelta(0,0,0,0,0,TimeSlotLength)





ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'
IdentConn = sqlite3.connect(ThesisRun_PATH+'HorusDB.db')
LogConn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Icc = IdentConn.cursor()
Lcc = LogConn.cursor()

def FindUser(Time,Victim,AttackSource,Fcc):
    UserList = []
    TimeCov = datetime.strptime(Time,"%Y-%m-%d %H:%M:%S")
    FUQuery = Fcc.execute('SELECT DISTINCT User FROM '+AcceptTable+' WHERE Time > ? AND Time < ? AND Source = ? AND IP = ?',(Time,TimeCov+SlotDuration,Victim,AttackSource))
    UserList = list(FUQuery)
    return UserList

def FindJoint(Time,Victim,AttackSource,Fcc,UserList):
    Jflag = 0
    TimeCov = datetime.strptime(Time,"%Y-%m-%d %H:%M:%S")
    TimeCov = TimeCov + 72 * SlotDuration
    for user in UserList:
        FJQuery = Fcc.execute('SELECT Time,IP FROM '+AcceptTable+' WHERE Time > ? AND Time < ? AND Source = ? AND User = ? AND IP != ?',(Time,TimeCov,Victim,user[0],AttackSource))
        if FJQuery is None:
            continue
        else:
            Jflag = 1
            FJList = list(FJQuery)
	    print 'Attacked User:',user[0]
	    print "===============================\n"
            for item in FJList:
		print "Joint attack time:",item[0]," | Joint attack IP:", item[1]
	FJUQuery = Fcc.execute('SELECT DISTINCT(IP) FROM '+AcceptTable+' WHERE Time > ? AND Time < ? AND Source = ? AND User = ? AND IP != ?',(Time,TimeCov,Victim,user[0],AttackSource))
        if FJUQuery is None:
            continue
        else:
            Jflag = 1
            FJUList = list(FJUQuery)
	    print 'IP Unique:'
	    print "===============================\n"
            for item in FJUList:
		print " | Joint attack IP:", item[0]


    return Jflag


#Target = raw_input('IP?:')
#Files = raw_input('file?:')
#fd = open(Files,'r')
#lines = fd.readlines()
def Identify_mod(line):
#for line in lines:
    Target = line.rstrip('\r\n')
    print Target, "Is identified as threat, report generating!"
    print "IP", Target
    BFAQuery = Icc.execute('SELECT Time,DstIP FROM IPObservation WHERE SrcIP = ? AND BFACount > 0',(Target,))

    print "IP brute force attack record:"
    for record in BFAQuery:
	print "Time:",record[0]," | Source IP:",record[1]

    print "===============================================\n"

    BFASQuery = Icc.execute('SELECT Time,DstIP FROM IPObservation WHERE SrcIP = ? AND BFASCount > 0',(Target,))

    print "Brute Force attack success record"
    for record in BFASQuery:
	print "BFAS data:", "\nAttack Time:", record[0],"\nAttacked Host:",record[1]
	UserList = FindUser(record[0],record[1],Target,Lcc)
	Jflag = FindJoint(record[0],record[1],Target,Lcc,UserList)

#    raw_input('Next?')
	
#    print "Users:", UserList

