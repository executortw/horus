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
record_try_failed = [["Foreign Address","first_time","last_time","count"],]
record_account_accepted = [["Account",["IP","Time"],["IP","Time"],"count"],]
while line != '':
    if DEBUG >= 1:
        print "\n========\nThe whole line taken in: \n", line
#    accepted_account = re.search("Accepted\skeyboard-interactive/pam\sfor\s([a-zA-Z0-9]*)\sfrom",line)
    accepted_account = re.search("((?<=Accepted keyboard-interactive/pam for )|(?<=Accepted publickey for ))[a-zA-Z0-9]*",line)
    try:
		#If "Accepted keyboard-interactive/pam for" is detected
        type(accepted_account.group(0))
        if DEBUG >=2:
            print "accepted_account.group(0):", accepted_account.group(0)
        IPident = re.search("(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|([a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*))",line)
        if DEBUG >= 3:
            print "Before the record was added:", record_account_accepted

        try:
            index = next((i for i, sublist in enumerate(record_account_accepted) if accepted_account.group(0) in sublist), -1)
            if index != -1:
			#if this account can be found in the list
                #index = record_try_failed.index(IPident.group(0))
                if DEBUG >= 2:
                    print "This Account has been checkin before.",accepted_account.group(0)
                Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
                login_ip_time = [IPident.group(0),Timeident.group(0)]
                record_account_accepted[index].append(login_ip_time)

                if DEBUG >= 3:
                    print "The record is added:" , record_account_accepted

            else:
			#if this account hasn't been seen
                if DEBUG >= 2:
                    print "This is the first time this Account has been seen.", accepted_account.group(0)
                Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
                login_ip_time = [IPident.group(0),Timeident.group(0)]
                new_record_account_accepted = [accepted_account.group(0),login_ip_time]
                if DEBUG >= 2:
                    print "new_record_account_accepted:",new_record_account_accepted
                record_account_accepted.append(new_record_account_accepted)
                if DEBUG >= 3:
                    print "The record is added:", record_account_accepted
			#If no IP has in the line.
        except AttributeError:
            if DEBUG >= 1:
                print "One alert without IP address just been processed"
                s = raw_input('-->')
            last_pos = process_file.tell()
            line = process_file.readline()
            continue

    except AttributeError:#no "Accepted password for root" has been found

        IPident = re.search("(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})|([a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*:[a-z0-9]*))",line)
        #First check this IP has been found or not.
        if DEBUG >= 3:
            print "Before the record was added:", record_try_failed

        try:
            index = next((i for i, sublist in enumerate(record_try_failed) if IPident.group(0) in sublist), -1)
            if index != 0:
			#if this IP can be found in the list
#		index = record_try_failed.index(IPident.group(0))
                if DEBUG >= 1:
                    print "This IP has been found before.",IPident.group(0)
                Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
                record_try_failed[index].append(Timeident.group(0))
                record_try_failed[index][3] = record_try_failed[index][3]+1
#                record_try_failed[index][2] = Timeident.group(0)
                if DEBUG >= 3:
                    print "The record is added:", record_try_failed
            else:
			#if this IP hasn't been seen.
                if DEBUG >= 1:
                    print "This is the first time this IP has been seen.",IPident.group(0)
                Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
                new_record_try_failed = [IPident.group(0),Timeident.group(0),Timeident.group(0),1]
                record_try_failed.append(new_record_try_failed)
                if DEBUG >= 3:
                    print "The record is added:", record_try_failed
			#If no IP has in the line.
        except AttributeError:
            if DEBUG >= 1:
                print "One alert without IP address just been processed"
                s = raw_input('-->')
            last_pos = process_file.tell()
            line = process_file.readline()
            continue

    if DEBUG >= 3:
        print "The end of the turn:",record_try_failed
        print "The end of the turn:",record_account_accepted

    if DEBUG >= 1:
            print "IP:", IPident.group(0)


    if DEBUG >= 1:
        Timeident = re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s[0-9]{1,2}\s[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}",line)
        print "Date:", Timeident.group(0)

    if DEBUG >= 3:
        s = raw_input('-->')

    last_pos = process_file.tell()
    line = process_file.readline()

print "\n\nResult record_try_failed matrix:"
#index = next(i for i, sublist in enumerate(record_try_failed)) 
for i in range(len(record_try_failed)):
    print record_try_failed[i][0]," ",record_try_failed[i][3]
#for i in range(len(record_try_failed)):
#    print record_try_failed[i][3]

ans = tuple(x[3] for x in record_try_failed)
print ans
#for data in record_try_failed:
#	print data[0], data[3]
#print record_try_failed[0], " " , record_try_failed[1], " " , record_try_failed[3]
print "\n\nResult record_account_accepted matrix:"
for data in record_account_accepted:
	print data
process_file.close()

