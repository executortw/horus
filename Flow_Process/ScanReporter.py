"""
This file is to read the scan report according to the netflow file, process it and send to database.
"""
"""
Argument dealing
"""

import sys
import os
import re
import EchoReader
import DatabaseModule
#Change this to adpat what file you are catching.
FileNameRegex = "ft-v05\.[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]{6}\+[0-9]{4}\.(?=possible_scan_source)"


if len(sys.argv) != 2:
	print "Usage:\n","\t>python ScanReporter.py <path>.\n","For example:\n\t>python ScanReporter.py /netflow/in/2012-04-26/ScanCount/"
else:
	path = sys.argv[1]
#	print path
	FileList = []
	os.chdir(path)
	Filenames = os.listdir(".")
	for eachfile in Filenames:
#		print eachfile,"\n"
		if re.match(FileNameRegex, eachfile) :
			FileList.append(eachfile)
#			print FileList
	
	FileList.sort()
	DailyEcho = EchoReader.EchoRead(FileList)

	#Get the DailyEcho list from EchoReader and send it to DatabaseModule
	for Echo in DailyEcho:
		DatabaseModule.EchointoDB(tuple(Echo))
