#!/bin/bash
./scanobserver.sh /netflow/in/2012-06-01
python ./ScanReporter.py /netflow/in/2012-06-01/ScanCount/
rm -rf /netflow/in/2012-06-01/ScanCount/
./scanobserver.sh /netflow/in/2012-06-02
python ./ScanReporter.py /netflow/in/2012-06-02/ScanCount/
rm -rf /netflow/in/2012-06-02/ScanCount/
./scanobserver.sh /netflow/in/2012-06-03
python ./ScanReporter.py /netflow/in/2012-06-03/ScanCount/
rm -rf /netflow/in/2012-06-03/ScanCount/
./scanobserver.sh /netflow/in/2012-06-04
python ./ScanReporter.py /netflow/in/2012-06-04/ScanCount/
rm -rf /netflow/in/2012-06-04/ScanCount/
./scanobserver.sh /netflow/in/2012-06-05
python ./ScanReporter.py /netflow/in/2012-06-05/ScanCount/
rm -rf /netflow/in/2012-06-05/ScanCount/
./scanobserver.sh /netflow/in/2012-06-06
python ./ScanReporter.py /netflow/in/2012-06-06/ScanCount/
rm -rf /netflow/in/2012-06-06/ScanCount/
./scanobserver.sh /netflow/in/2012-06-07
python ./ScanReporter.py /netflow/in/2012-06-07/ScanCount/
rm -rf /netflow/in/2012-06-07/ScanCount/
./scanobserver.sh /netflow/in/2012-06-08
python ./ScanReporter.py /netflow/in/2012-06-08/ScanCount/
rm -rf /netflow/in/2012-06-08/ScanCount/
./scanobserver.sh /netflow/in/2012-06-09
python ./ScanReporter.py /netflow/in/2012-06-09/ScanCount/
rm -rf /netflow/in/2012-06-09/ScanCount/
./scanobserver.sh /netflow/in/2012-06-10
python ./ScanReporter.py /netflow/in/2012-06-10/ScanCount/
rm -rf /netflow/in/2012-06-10/ScanCount/
./scanobserver.sh /netflow/in/2012-06-11
python ./ScanReporter.py /netflow/in/2012-06-11/ScanCount/
rm -rf /netflow/in/2012-06-11/ScanCount/


