DEBUG = 0
try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"
from datetime import datetime



def EchointoDB(Tuple):
	conn = sqlite3.connect('/home/executor/Thesis_run/HorusDB.db')
	cc = conn.cursor()
	cc.execute('CREATE TABLE IF NOT EXISTS IPObservation ( Time text(100), SrcIP text(100), DstIP text(100) DEFAULT [0], ScanCount integer DEFAULT [0], BFACount integer DEFAULT [0], BFASCount BOOLEAN DEFAULT [0], LoginCount integer DEFAULT [0])')
	cc.close()
	conn.commit()
	"""DB Connection"""
	Echoconn = sqlite3.connect('/home/executor/Thesis_run/HorusDB.db')
	Ecc = Echoconn.cursor()


	Records = list(Tuple)
	Temp = Records[0]
	Timesplit = Temp.split("-")
	DHsplit = Timesplit[2].split(".")
	Time = datetime(int(Timesplit[0]),int(Timesplit[1]),int(DHsplit[0]),int(DHsplit[1]))

	Records.remove(Temp)

	for record in Records:
		IP = record[0]
		Counts = record[1]
		#if Time+IP exist, update it(other program might insert it before I do)
		Ecc.execute("SELECT ScanCount FROM IPObservation WHERE Time = ? AND SrcIP = ?",(Time,IP))
		verify = Ecc.fetchone()
		if verify is None:
			Ecc.execute('INSERT INTO IPObservation(Time,SrcIP,ScanCount) VALUES (?,?,?)',(Time,IP,Counts))
		else:
#			print verify
			NumCounts = Counts + verify[0]
			Ecc.execute('UPDATE IPObservation SET ScanCount = (?) WHERE Time = ? AND SrcIP = ?',(NumCounts, Time,IP))
#		Ecc.execute("IF EXISTS (SELECT * FROM IPObservation WHERE Time == (?) AND IP == (?)) UPDATE IPObservation SET ScanCount = (?) WHERE Time == (?) AND IP == (?) ELSE INSERT INTO IPObservation(Time,SrcIP,ScanCount) VALUES (?,?,?)",(Time,IP,Counts,Time,IP,Time,IP,Counts))
		#if Time+IP doesn't exist, insert it.
#		Ecc.execute("INSERT INTO IPObservation(Time,SrcIP,ScanCount) VALUES (?,?,?,?)",(Time,IP,Counts))
	Ecc.close()
	Echoconn.commit()


