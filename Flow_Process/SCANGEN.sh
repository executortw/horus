#!/bin/bash
for i in {1..30}; 
do 
    echo ./scanobserver.sh /netflow/in/2012-05-$i > ./SCAN.sh; 
    echo python ./ScanReporter.py /netflow/in/2012-05-$1/ScanCount/ > ./SCAN.sh; 
done;
