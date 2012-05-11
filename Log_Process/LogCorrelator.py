

try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"
from datetime import datetime
from datetime import timedelta

ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'
DEBUG = 0
#The duration of one phase/timeslot is set by TimeSlotLength
TimeSlotLength = 1
Threshold_Number_of_Attempts = 10#Threshold of number of each IP trying to attack host
Threshold_Number_of_Users = 3 #Threshold of number of each IP trying to login with users

#Mark either the BFA or the BFAS or the Login
def StatusMarker(Qcc,SlotStart,Period,IP,STATUS):
    #
    Horusconn = sqlite3.connect(ThesisRun_PATH+'HorusDB.db')
    Hcc = Horusconn.cursor()

    Hcc.execute('CREATE TABLE IF NOT EXISTS IPObservation ( Time text(100), SrcIP text(100), DstIP text(100) DEFAULT [0], ScanCount integer DEFAULT [0], BFACount integer DEFAULT [0], BFASCount BOOLEAN DEFAULT [0], LoginCount integer DEFAULT [0])') 
    #The STATUS makes difference here, BFA/LOGIN will update IPObservation differently.
    if STATUS == 'BFA':
	Hcc.execute('SELECT BFACount FROM IPObservation WHERE Time = ? AND SrcIP = ? AND DstIP = ?',(SlotStart,IP[1],IP[0]))
        verify = Hcc.fetchone()
        if verify is None:
	    #This record hasn't been record yet.
	    Hcc.execute('INSERT INTO IPObservation(Time,SrcIP,DstIP,BFACount) VALUES (?,?,?,?)',(SlotStart,IP[1],IP[0],1))
        else:
	    #Update the record
	    Hcc.execute('UPDATE IPObservation SET BFACount = ? WHERE Time = ? AND SrcIP = ? AND DstIP = ?',(verify[0]+1,SlotStart,IP[1],IP[0]))
    elif STATUS == 'LOGIN':
	Hcc.execute('SELECT LoginCount FROM IPObservation WHERE Time = ? AND SrcIP = ? AND DstIP = ?',(SlotStart,IP[1],IP[0]))
        verify = Hcc.fetchone()
        if verify is None:
	    #This record hasn't been record yet.
	    Hcc.execute('INSERT INTO IPObservation(Time,SrcIP,DstIP,LoginCount) VALUES (?,?,?,?)',(SlotStart,IP[1],IP[0],1))
        else:
	    #Update the record
	    Hcc.execute('UPDATE IPObservation SET LoginCount = ? WHERE Time = ? AND SrcIP = ? AND DstIP = ?',(verify[0]+1,SlotStart,IP[1],IP[0]))
    Hcc.close()
    Horusconn.commit()


#Find the date of the first record and the last record, counting them according to the records.
def Timefinder(Qcc,TableName):
    Qcc.execute("SELECT Time FROM "+TableName+" ORDER BY Time ASC")
    record = Qcc.fetchone()
    StarTime = datetime.strptime(record[0],"%Y-%m-%d %H:%M:%S")
#    StarTime.minute = time.second = 0
    Qcc.execute("SELECT Time FROM "+TableName+" ORDER BY Time DESC")
    record = Qcc.fetchone()
    EndTime = datetime.strptime(record[0],"%Y-%m-%d %H:%M:%S")
#    EndTime.minute = time.second = 0
    return (StarTime,EndTime)

#BFADetector
def LogCounter(Qcc,StarTime,EndTime,TableName,Type):
    #First, how many time slot we are dealing here?
    if DEBUG >= 3:
        print StarTime , EndTime
	print EndTime - StarTime
    #We don't need the mins and seconds	
    SlotStart = datetime(StarTime.year,StarTime.month,StarTime.day,StarTime.hour)
    SlotEnd = datetime(EndTime.year,EndTime.month,EndTime.day,EndTime.hour)
    #Find the delta between SlotEnd and SlotStart
    StarttoEnd = SlotEnd - SlotStart
    SlotNumber = StarttoEnd.days * 24 + StarttoEnd.seconds/3600#divided by 3600 to get the hours
    if DEBUG >= 2:
        print "SlotNumber:", SlotNumber
    #The duration of one phase/timeslot is set by TimeSlotLength
    SlotDuration = timedelta(0,0,0,0,0,TimeSlotLength)

    #Let's count data in each slot
    for i in range(SlotNumber):
	#Seperate Failed and Accept from here, Failed to count BFA , Accept to count success login
	if Type == "Failed":
	    #2 Check flag: TooManyTries and TooManyAccounts
	    TooManyTries = 0
	    TooManyAccounts = 0

	    if DEBUG >= 1:
	       print SlotStart, SlotStart+SlotDuration
	    #Get the attackers from the database in this time slot
	    AttackIPs = Qcc.execute("SELECT DISTINCT Source,IP FROM "+TableName+" WHERE Time > ? AND Time < ?",(SlotStart,SlotStart+SlotDuration))
	    #If no attacker in this time slot
	    if AttackIPs is None:
		continue
	    else:
		for IP in AttackIPs:	
		    TooManyTries = 0
		    TooManyAccounts = 0

		    #Find time of login attemps tried by each attacker
		    Qcc.execute("SELECT COUNT(IP) FROM "+TableName+" WHERE Source = ? AND IP = ?",(IP[0],IP[1]))
		    AttackNum = Qcc.fetchone()
		    if DEBUG >= 2:
			print "IP:", IP, "Attack Time:", AttackNum
		    #If one IP tried over Threshold_Number_of_Attempts times we said we are BFA.
		    if AttackNum >= Threshold_Number_of_Attempts:
			TooManyTries = 1
		    #We want to know how many user has been tried by the IP in one time slot
		    Qcc.execute("SELECT COUNT(DISTINCT User) FROM "+TableName+" WHERE Source = ? AND  IP = ?",(IP[0],IP[1]))
		    NumberofUser = Qcc.fetchone()
		    if DEBUG >= 2:
			print "IP:", IP, "User tried:", NumberofUser
		    #If one IP tried to login with too many user(over the Threshold_Number_of_Users) we said we are BFA
		    if NumberofUser >= Threshold_Number_of_Users:
			TooManyAccounts = 1

		    #We could change the alert decision here.
		    if TooManyTries or TooManyAccounts:
			print "BFA!",IP[0],"is BFA by ",IP[1],"! in ", SlotStart, SlotStart+SlotDuration
			StatusMarker(Qcc,SlotStart,SlotStart+SlotDuration,IP,"BFA")

	    #We add SlotDuration to SlotStart to push the timestamp forward
	    SlotStart = SlotStart + SlotDuration
	elif Type == "Accept":
	    print SlotStart, SlotStart+SlotDuration
	    AcceptIPs = Qcc.execute("SELECT DISTINCT Source,IP FROM "+TableName+" WHERE Time > ? AND Time < ?",(SlotStart,SlotStart+SlotDuration))
	    if AcceptIPs is None:
		continue
	    else:
		for IP in AcceptIPs:
		    print IP[0],"Logged In" 
		    StatusMarker(Qcc,SlotStart,SlotStart+SlotDuration,IP,"LOGIN")
		    """
		    Qcc.execute("SELECT COUNT(Time) FROM "+TableName+" WHERE IP = ?",(IP))
		    count =  Qcc.fetchone()
		    print count
		    result = Qcc.execute("SELECT IP,User FROM "+TableName+" WHERE IP = ?",(IP))
		    for log in result:
			print log
		    """
#	    print "Here for Accept Function"
	    SlotStart = SlotStart + SlotDuration

#MAIN
Queryconn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Qcc = Queryconn.cursor()
FailedIP = []

#Check if the table is exist or not
Qcc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(FailedTable,))
verify = Qcc.fetchone()
if verify is None:
#If the table is not exist
    print "The '%s' table is not exist" %(FailedTable)
else:
#The table exist, keep working...
#Find the date through Timefinder for now, the StarTime, EndTime could be set by other methods in the future.
    StarTime, EndTime = Timefinder(Qcc,FailedTable)
    LogCounter(Qcc,StarTime,EndTime,FailedTable,"Failed")

#Check if the table is exist or not
Qcc.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(AcceptTable,))
verify = Qcc.fetchone()
if verify is None:
#If the table is not exist
    print "The '%s' table is not exist" %(AcceptTable)
else:
#The table exist, keep working...
#Find the date through Timefinder for now, the StarTime, EndTime could be set by other methods in the future.
    StarTime, EndTime = Timefinder(Qcc,AcceptTable)
    LogCounter(Qcc,StarTime,EndTime,AcceptTable,"Accept")



Qcc.close()
Queryconn.commit()
