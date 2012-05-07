#!/bin/bash
mkdir flowrpt-ip-port
for file in ./*
do
	echo ${file}
	flow-cat "${file}" | flow-report -v TYPE=ip-source-address/ip-source/destination-port > "./flowrpt-ip-port/${file}.ip-port"
	
done
