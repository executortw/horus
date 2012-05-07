#!/bin/bash
#Usage: scanobserver.sh <Netflow data path>
#Example: scanobserver.sh /netflow/in/2012-04-27
PingThreshold=50
#Connection more than $PingThreshold in 10 mins will be found
DataFolder="ScanCount"
#I save the ip-port netflow report file in Directory DataFolder the ip-port netflow report file show the src, ip, and src, dst port mapping record.
#So I could find the ICMP connection in the netflow records.
#The DataFolder should be created in the netflow file folder.
#<Maybe should be delete after everything is done?>
TargetPath=$1
#TargetPath means the storage path of the netflow files to be processed.
#
#echo "$TargetPath"
regex="(ft-v05\.[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]{6}\+[0-9]{4})"
cd $TargetPath
mkdir $DataFolder
for file in *
do
#	echo ${file}
#	echo "$regex"
	if [[ ${file} =~ $regex ]]; then
		flow-cat "${file}" | flow-report -v TYPE=ip-source-address/ip-source/destination-port > "$TargetPath/$DataFolder/${file}.ip-port"
		#Here we use the flow-cat command and flow-report to make a report f each netflow files, to find the src,dst ip and port correlation.
		awk '{if ($2 == $3 && $3 == 0 && $4 >= '$PingThreshold' ) {print $1" "$4} }' "$TargetPath/$DataFolder/${file}.ip-port" | sort > "$TargetPath/$DataFolder/${file}.possible_scan_source"
		#Then I check whether the src and dst port are bother equal to "0" means the src ip "ping" dst ip, and I find those ip which have more than $PingThreshold connection in 10mins, output to <netflow file>.possible_scan_source
	else
		echo "Doesn't match"
	fi
done
