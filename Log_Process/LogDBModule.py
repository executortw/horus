DEBUG = 0
try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"

def LogintoDB(failed_logins,accept_logins,Source):
    conn = sqlite3.connect('IPDB.db')
    cc = conn.cursor()

    cc.execute('CREATE TABLE IF NOT EXISTS FailedRecord ( Source text(100), Time timestamp(8), IP text(100), User text(100), Count integer DEFAULT [0])')
    cc.execute('CREATE TABLE IF NOT EXISTS AcceptRecord ( Source text(100), Time timestamp(8), IP text(100), User text(100), Count integer DEFAULT [0])')
    """DB Connection"""

    Logconn = sqlite3.connect('IPDB.db')
    Lcc = Logconn.cursor()

    for record in failed_logins:
	Time = record[0]
	IP = record[1]
	User = record[2]
	#If Time+IP+ID exist, don't insert again, just count it.
	Lcc.execute("SELECT Count FROM FailedRecord WHERE Source = ? AND Time = ? AND IP = ? AND User = ?",(Source, Time,IP,User))
	verify = Lcc.fetchone()
	if verify is None:
	    Lcc.execute('INSERT INTO FailedRecord(Source, Time,IP,User) VALUES (?, ?,?,?)',(Source, Time,IP,User))
	else:
	    Count = verify[0] + 1
	    Lcc.execute('UPDATE FailedRecord SET Count = ? WHERE Source = ? AND Time = ? AND IP = ? AND User = ?',(Source, Count,Time,IP,User))

    for record in accept_logins:
	Time = record[0]
	IP = record[1]
	User = record[2]
	#If Time+IP+ID exist, don't insert again, just count it.
	Lcc.execute("SELECT Count FROM AcceptRecord WHERE Source = ? AND Time = ? AND IP = ? AND User = ?",(Source, Time,IP,User))
	verify = Lcc.fetchone()
	if verify is None:
	    Lcc.execute('INSERT INTO AcceptRecord(Source, Time,IP,User) VALUES (?,?,?,?)',(Source,Time,IP,User))
	else:
	    Count = verify[0] + 1
	    Lcc.execute('UPDATE AcceptRecord SET Count = ? WHERE Source = ? AND Time = ? AND IP = ? AND User = ?',(Source,Count,Time,IP,User))

    Lcc.close()
    Logconn.commit()
#	Ecc.execute("IF NOT EXISTS (SELECT * FROM FailedRecord WHERE Time = ? AND IP = ? AND User = ?) INSERT INTO FailedRecord(Time,IP,User) VALUES (?,?,?) \
#		ELSE UPDATE FailedRecord SET ",(record[0],record[1],record[2],record[0],record[1],record[2]))


