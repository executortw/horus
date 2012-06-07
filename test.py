try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"
import os




ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'
Horusconn = sqlite3.connect(ThesisRun_PATH+'HorusDB.db')
Hcc = Horusconn.cursor()
#FindUserconn > FUconn
FUconn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Fcc = FUconn.cursor()

fd = open('IPList','r')

#CheckIP = raw_input("IP?")
for line in fd:
    SPLIT = line.split('\n')
    CheckIP = SPLIT[0]
    print CheckIP
#    while(CheckIP != None):
    Number = Fcc.execute('SELECT COUNT(DISTINCT Time) FROM FailedRecord WHERE IP = ?',(CheckIP,))
    for i in list(Number):
	print i
    Result = Fcc.execute('SELECT * FROM FailedRecord WHERE IP = ?',(CheckIP,))
    for record in list(Result):
	print record
    Number = Fcc.execute('SELECT COUNT(DISTINCT Time) FROM FailedRecord WHERE IP = ?',(CheckIP,))
    for i in list(Number):
	print i

    Result = Fcc.execute('SELECT DISTINCT user FROM FailedRecord WHERE IP = ?',(CheckIP,))
    for record in list(Result):
	print record

    print "Accept:"
    Result = Fcc.execute('SELECT DISTINCT user FROM AcceptRecord WHERE IP = ?',(CheckIP,))
    for record in list(Result):
	print record

    print CheckIP
    raw_input("Next?")


Fcc.close()
FUconn.commit()
