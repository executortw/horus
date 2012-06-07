#!/bin/bash
./scanobserver.sh /netflow/in/2012-05-10
python ./ScanReporter.py /netflow/in/2012-05-10/ScanCount/
./scanobserver.sh /netflow/in/2012-05-11
python ./ScanReporter.py /netflow/in/2012-05-11/ScanCount/
./scanobserver.sh /netflow/in/2012-05-12
python ./ScanReporter.py /netflow/in/2012-05-12/ScanCount/
./scanobserver.sh /netflow/in/2012-05-13
python ./ScanReporter.py /netflow/in/2012-05-13/ScanCount/
./scanobserver.sh /netflow/in/2012-05-14
python ./ScanReporter.py /netflow/in/2012-05-14/ScanCount/
./scanobserver.sh /netflow/in/2012-05-15
python ./ScanReporter.py /netflow/in/2012-05-15/ScanCount/
./scanobserver.sh /netflow/in/2012-05-16
python ./ScanReporter.py /netflow/in/2012-05-16/ScanCount/
./scanobserver.sh /netflow/in/2012-05-17
python ./ScanReporter.py /netflow/in/2012-05-17/ScanCount/
./scanobserver.sh /netflow/in/2012-05-18
python ./ScanReporter.py /netflow/in/2012-05-18/ScanCount/
./scanobserver.sh /netflow/in/2012-05-19
python ./ScanReporter.py /netflow/in/2012-05-19/ScanCount/

