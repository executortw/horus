#!/bin/bash
./scanobserver.sh /netflow/lab/2012-04-17
python ./ScanReporter.py /netflow/lab/2012-04-17/ScanCount/
./scanobserver.sh /netflow/lab/2012-04-18
python ./ScanReporter.py /netflow/lab/2012-04-18/ScanCount/
./scanobserver.sh /netflow/lab/2012-04-19
python ./ScanReporter.py /netflow/lab/2012-04-19/ScanCount/
./scanobserver.sh /netflow/lab/2012-04-20
python ./ScanReporter.py /netflow/lab/2012-04-20/ScanCount/
./scanobserver.sh /netflow/lab/2012-04-21
python ./ScanReporter.py /netflow/lab/2012-04-21/ScanCount/

