import os
import re
import DatabaseModule
DEBUG = 0 
#DEBUG: 0 means close/rough, 1 means low, 2 means medium, 3 means high/detail

def EchoRead(FileList):
#	print FileList
	EchoTotal = open('./EchoTotal','w')
	DailyEcho = []
	"""
	DailyEcho:[["Hour of the file",["IP","Number of Echo"],],]
	"""

	for filename in FileList:
		"""
		Here we store each file into the EchoTotal seperately
		"""
		"""
		try:
			print filename
			Time = re.search("(?<=ft-v05\.)[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]{6}",filename)
			EchoReadFile = open(filename)
			TimeString = Time.group(0) + "\n"
			EchoTotal.write(TimeString)
			for line in EchoReadFile:
				EchoSplit = line.split(" ")
				print EchoSplit
				EchoTotal.write(line)
		except IOError:
			continue
		"""
		"""
		End
		"""
		"""
		Here we count the number of echo from each IP by certain period.
		The period is 1 hour.
		"""

		try:
			Time = re.search("(?<=ft-v05\.)[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]{2}(?=[0-9]{4})",filename)
			EchoReadFile = open(filename)
			Hour = Time.group(0)

			index = next((i for i, sublist in enumerate(DailyEcho) if Hour in sublist), -1)

			if index == -1:
			#If the hour of what we are dealing with is not exist in the DailyEcho...
				HourlyEcho = [Hour,]
				"""
				HourlyEcho:[Hour,["IP","Number of Echo"],]
				"""
				for line in EchoReadFile:
					EchoSplit = line.split(" ")

					nested_index = next((i for i, sublist in enumerate(HourlyEcho) if EchoSplit[0] in sublist), -1)

					if nested_index != -1:
					#Once we found the ip has been recorded in this hour, we add the number of echo into the record.
						if DEBUG >= 3:
							print "IP:", EchoSplit[0]
							print "Echo Number:", EchoSplit[1]
						HourlyEcho[nested_index][1] = HourlyEcho[nested_index][1] + int(EchoSplit[1])
					else:
					#If the ip hasn't been recorded before, record it and put the number into the list
						if DEBUG >= 3:
							print "IP:", EchoSplit[0]
							print "Echo Number:", EchoSplit[1]
						AppendingList = [EchoSplit[0],int(EchoSplit[1])]
						HourlyEcho.append(AppendingList)

				DailyEcho.append(HourlyEcho)

			else:
			#If the hour of what we are dealing with is already exist in the DailyEcho...
				for line in EchoReadFile:
					EchoSplit = line.split(" ")

					nested_index = next((i for i, sublist in enumerate(DailyEcho[index]) if EchoSplit[0] in sublist), -1)

					if nested_index != -1:
					#Once we found the ip has been recorded in this hour, we add the number of echo into the record.
						if DEBUG >= 3:
							print "IP:", EchoSplit[0]
							print "Echo Number:", EchoSplit[1]
						DailyEcho[index][nested_index][1] = DailyEcho[index][nested_index][1] + int(EchoSplit[1])
					else:
					#If the ip hasn't been recorded before, record it and put the number into the list
						if DEBUG >= 3:
							print "IP:", EchoSplit[0]
							print "Echo Number:", EchoSplit[1]
						AppendingList = [EchoSplit[0],int(EchoSplit[1])]
						DailyEcho[index].append(AppendingList)

			if DEBUG >= 2:
				print "HourlyEcho:", DailyEcho

		except IOError:
			continue
	"""
	So now I get a array called DailyEcho which record IP<->Echo Number mapping of each hour. What I do now? 
	Maybe put into a file or into the database.
	"""
	"""
	You can see the array from this DEBUG mechanism
	"""
	if DEBUG >=1:
		for Hour in DailyEcho:
			print Hour
#			EchoTotal.write(Hour)

	"""
	end
	"""
	return DailyEcho
#	for Echo in DailyEcho:
#		Tuple = tuple(Echo)
#	print Tuple
#	List = list(Tuple)
#	print List
#		DatabaseModule.EchointoDB(Tuple)



