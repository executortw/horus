"""
This file read Obfile( by specifying filename, due to you could choose obfile by different file of date.), to process the Observation in Obfile and the IP.
Output in format of IP:<Observations>
April/2012 executor
Modified: Import Detection Module. Let the detection module deal with the observation string. 

"""
import os
import re
import Detection
import Identify_module


try:
    try:
        from pysqlite2 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3
except ImportError:
    print "sqlite3 or pysqlite2 not found"


ThesisRun_PATH = '/home/executor/Thesis_run/'
FailedTable = 'FailedRecord'
AcceptTable = 'AcceptRecord'

IPList = []
IPList2 = []
AlertList = []
AppendList = []
IdentSwitch = "N"
IdentOrNot = "N"
PrintOrNot = "N"
Obfile = raw_input('Obfile name?:')
fd = open(Obfile,'r')

switch = 2
switch = raw_input('Which Mode to choose?(1/2):')
#Connection Combination mode choose, 1 for localhost->attacker source combination, 2 for attacker source->localhost combination 2 is recommended.
if switch == 1:
    for line in fd:
	LineSplit = line.split("|")
	Number = re.search('[1-5]',LineSplit[3])
    #    index = next((i for i , sublist in enumerate(IPList) if LineSplit[2] in sublist), -1)
	index = next((i for i , sublist in enumerate(IPList) if LineSplit[1] in sublist), -1)
	if index != -1:
    #	AppendList = []
    #	index2 = next((i for i , sublist in enumerate(IPList[index]) if LineSplit[1] in sublist), -1)
	    index2 = next((i for i , sublist in enumerate(IPList[index]) if LineSplit[2] in sublist), -1)
	    if index2 != -1:
		IPList[index][index2].append(Number.group(0))
	    else:
    #	    AppendList = [LineSplit[1],Number.group(0)]
		AppendList = [LineSplit[2],Number.group(0)]
		IPList[index].append(AppendList)
	else:
    #	AppendList = []
    #	AppendList = [LineSplit[1],Number.group(0)]
    #	NewRecord = [LineSplit[2],AppendList]
	    AppendList = [LineSplit[2],Number.group(0)]
	    NewRecord = [LineSplit[1],AppendList]

	    IPList.append(NewRecord)
    IPList.sort()
else:
    for line in fd:
	LineSplit = line.split("|")
	Number = re.search('[1-5]',LineSplit[3])
	index = next((i for i , sublist in enumerate(IPList) if LineSplit[2] in sublist), -1)
    #    index = next((i for i , sublist in enumerate(IPList) if LineSplit[1] in sublist), -1)
	if index != -1:
    #	AppendList = []
	    index2 = next((j for j , sublist in enumerate(IPList[index]) if LineSplit[1] in sublist), -1)
    #	index2 = next((i for i , sublist in enumerate(IPList[index]) if LineSplit[2] in sublist), -1)
	    if index2 != -1:
		if index2 == 0:
#		    print type(IPList[index][index2]), IPList[index], IPList[index][index2],index2
		    index2 = 1
		IPList[index][index2].append(Number.group(0))
	    else:
		AppendList = [LineSplit[1],Number.group(0)]
    #	    AppendList = [LineSplit[2],Number.group(0)]
		IPList[index].append(AppendList)
	else:
	    AppendList = []
	    AppendList = [LineSplit[1],Number.group(0)]
	    NewRecord = [LineSplit[2],AppendList]
#	    print NewRecord
    #	AppendList = [LineSplit[2],Number.group(0)]
    #	NewRecord = [LineSplit[1],AppendList]

	    IPList.append(NewRecord)
    IPList.sort()

FUconn = sqlite3.connect(ThesisRun_PATH+'HorusLog.db')
Fcc = FUconn.cursor()
ItemNumber = len(IPList)
IPPair = {}
ASource = IPList[0] 
IdentSwitch = raw_input("[Evaluation]Do you need to Ident the IPPair?(y/N)")
if IdentSwitch == 'Y' or IdentSwitch == 'y' :
    for i in range(len(IPList)):
	for j in range(len(IPList[i])-1):
	    Connection = IPList[i][0] +"<->"+ IPList[i][j+1][0]
	    FQresult = Fcc.execute('SELECT * FROM '+FailedTable+' WHERE Source = ? AND IP = ?',(IPList[i][j+1][0],IPList[i][0]))
	    print 'Failed Record:'
	    for record in list(FQresult):
	       print record
	    ACresult = Fcc.execute('SELECT * FROM '+AcceptTable+' WHERE Source = ? AND IP = ?',(IPList[i][j+1][0],IPList[i][0]))
	    print 'Accept Record:'
	    for record in list(ACresult):
	       print record
	    Question = 'What condiction '+Connection+' is? Negative(0),Positive(1)'
	    Ident = raw_input(Question)
	    IPPair[Connection] = Ident
"""
	AppendArr = [IPList[i][0],IPList[i][j+1][0]]
	IPPair.append(AppendArr)"""


fd = open('ObCon-Tag','w')
fd2 = open('ConIdent','w')



#keys = IPPair.viewkeys()
#print '\nIPList'
#fd2.write('IPList Result:\n')


for sublist in IPList:
    if len(sublist) < 0:
	continue
    IP = sublist.pop(0)
    for subsublist in sublist:
	subsublist.pop(0)
#	print "poped subsublist",subsublist
	if Detection.Detection(IP,subsublist) == 1:
	    AlertList.append(IP)
	    break
	else:
	    continue
IdentOrNot = raw_input("Do you want to identify alert list? (y/N) ")
if IdentOrNot == "y":
    for IP in AlertList:
	Identify_module.Identify_mod(IP)
else:
    PrintOrNot = raw_input("Do list need to be printed? (y/N) ")
    if PrintOrNot == "y":
	print "AlertList:"
	for IP in AlertList:
	    print IP
    
fd.close()
fd2.close()
