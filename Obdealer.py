import os
import re

IPList = []
AppendList = []
Obfile = raw_input('Obfile name?:')
fd = open(Obfile,'r')
for line in fd:
    LineSplit = line.split("|")
    Number = re.search('[1-5]',LineSplit[3])
    index = next((i for i , sublist in enumerate(IPList) if LineSplit[2] in sublist), -1)
    if index != -1:
#	AppendList = []
	index2 = next((i for i , sublist in enumerate(IPList[index]) if LineSplit[1] in sublist), -1)
	if index2 != -1:
	    IPList[index][index2].append(Number.group(0))
	else:
	    AppendList = [LineSplit[1],Number.group(0)]
	    IPList[index].append(AppendList)
    else:
#	AppendList = []
	AppendList = [LineSplit[1],Number.group(0)]
	NewRecord = [LineSplit[2],AppendList]
	IPList.append(NewRecord)
IPList.sort()
for item in IPList:
#    if len(item) < 5:
#	continue
    for key in item:
	print key
    print "\n"

