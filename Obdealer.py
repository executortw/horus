import os
import re

IPList = []
AppendList = []
fd = open('Obfile','r')
for line in fd:
    LineSplit = line.split("|")
    Number = re.search('[1-5]',LineSplit[2])
    index = next((i for i , sublist in enumerate(IPList) if LineSplit[1] in sublist), -1)
    if index != -1:
#	AppendList = []
#	AppendList = [LineSplit[0],Number.group(0)]
	IPList[index].append(Number.group(0))
    else:
#	AppendList = []
#	AppendList = [LineSplit[0],Number.group(0)]
	NewRecord = [LineSplit[1],Number.group(0)]
	IPList.append(NewRecord)
IPList.sort()
for item in IPList:
    if len(item) < 5:
	continue
    for key in item:
	print key,
    print "\n"

