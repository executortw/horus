try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"


Queryconn = sqlite3.connect('/home/executor/Thesis_run/HorusDB.db')
Qcc = Queryconn.cursor()
AttackIPs = Qcc.execute("SELECT * FROM IPObservation WHERE BFASCount != 0 OR LoginCount != 0 ORDER BY Time ASC;")
for IP in AttackIPs:
    print IP

Qcc.close()
Queryconn.commit()

