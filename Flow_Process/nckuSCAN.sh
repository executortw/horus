#!/bin/bash
./scanobserver.sh /netflow/ncku-csie/2012-04-18
python ./ScanReporter.py /netflow/ncku-csie/2012-04-18/ScanCount/
./scanobserver.sh /netflow/ncku-csie/2012-04-19
python ./ScanReporter.py /netflow/ncku-csie/2012-04-19/ScanCount/
./scanobserver.sh /netflow/ncku-csie/2012-04-20
python ./ScanReporter.py /netflow/ncku-csie/2012-04-20/ScanCount/
./scanobserver.sh /netflow/ncku-csie/2012-04-21
python ./ScanReporter.py /netflow/ncku-csie/2012-04-21/ScanCount/
./scanobserver.sh /netflow/ncku-csie/2012-04-22
python ./ScanReporter.py /netflow/ncku-csie/2012-04-22/ScanCount/

