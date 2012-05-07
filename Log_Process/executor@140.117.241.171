#log_process.py
"""
This file log_process is used to process the logs from syslog,
to identify these attacker whether has been detected, and what is 
the start time of the attack, and the end time of the attack.

future work: save each attack log from different attacker to different log file,such as attack from 140.117.194.229 save to file log_140.117.194.229, in order to make it easier to read if we wish to take a look at what the attacker really do, and to see if the last attacking log is success or not.

This program is made by Executor.
"""
DEBUG = 0

import sys
import os
import re

arg = sys.argv
process_file = open(arg[1])
last_pos = process_file.tell()
line = process_file.readline()
record_try_failed = [["Foreign Address","first_time","last_time"],]
record_root_accepted = [["IP","Appended Accepted Time"],]
while line != '':
	if DEBUG == 1:
		print "The whole line taken in: \n", line
	accepted_or_not = re.search("(Accepted password for root)",line)
	try:
		#If "Accepted password for root" is detected
		type(accepted_or_not.group(0))
		IPident = re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",line)
		if DEBUG == 2:
			print record_try_failed

		try:
			index = next((i for i, sublist in enumerate(record_root_accepted) if IPident.group(0) in sublist), -1)
			if index != -1:
			#if this IP can be found in the list
#		index = record_try_failed.index(IPident.group(0))
				print "This IP has been found before."
				Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
				record_root_accepted[index].append(Timeident.group(0))

				if DEBUG == 1:
					print record_root_accepted

			else:
			#if this IP hasn't been seen
				print "This is the first time this IP has been seen."
				Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
				new_record_root_accepted = [IPident.group(0),Timeident.group(0)]
				record_root_accepted.append(new_record_root_accepted)
				if DEBUG == 1:
					print record_root_accepted
			#If no IP has in the line.
		except AttributeError:
			if DEBUG == 1:
				print "One alert without IP address just been processed"
				s = raw_input('-->')
			last_pos = process_file.tell()
			line = process_file.readline()
			continue

	except AttributeError:#no "Accepted password for root" has been found

		IPident = re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})",line)
		#First check this IP has been found or not.
		if DEBUG == 2:
			print record_try_failed

		try:
			index = next((i for i, sublist in enumerate(record_try_failed) if IPident.group(0) in sublist), -1)
			if index != -1:
			#if this IP can be found in the list
#		index = record_try_failed.index(IPident.group(0))
			
			
				print "This IP has been found before."
				Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
				record_try_failed[index][2] = Timeident.group(0)
				if DEBUG == 1:
					print record_try_failed
			else:
			#if this IP hasn't been seen.
				print "This is the first time this IP has been seen."
				Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
				new_record_try_failed = [IPident.group(0),Timeident.group(0),Timeident.group(0)]
				record_try_failed.append(new_record_try_failed)
				if DEBUG == 1:
					print record_try_failed
			#If no IP has in the line.
		except AttributeError:
			if DEBUG == 1:
				print "One alert without IP address just been processed"
				s = raw_input('-->')
			last_pos = process_file.tell()
			line = process_file.readline()
			continue

	if DEBUG == 2:
		print record_try_failed

	if DEBUG == 1:
		print "IP:", IPident.group(0)


	if DEBUG == 1:
		Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
		print "Date:", Timeident.group(0)

	if DEBUG == 1:
		s = raw_input('-->')

	last_pos = process_file.tell()
	line = process_file.readline()

print "Result record_try_failed matrix:"
for data in record_try_failed:
	print data
print "Result record_root_accepted matrix:"
for data in record_root_accepted:
	print data
process_file.close()

