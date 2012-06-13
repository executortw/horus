#!/bin/bash
python LogProcessor.py /var/log/long/1.log 140.117.205.1
mv /var/log/long/1.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/5.log 140.117.205.5
mv /var/log/long/5.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/10.log 140.117.205.10
mv /var/log/long/10.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/205-245.log 140.117.205.245
mv /var/log/long/205-245.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/140-127-220-54-long.log 140.127.220.54
mv /var/log/long/140-127-220-54-long.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/172.log 140.117.241.172
mv /var/log/long/172.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/173.log 140.117.241.173
mv /var/log/long/173.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/175.log 140.117.241.175
mv /var/log/long/175.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/230.log 140.117.241.230
mv /var/log/long/230.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/178-238.log 140.117.178.238
mv /var/log/long/178-238.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/ncku-csie-246-202-long.log 140.116.246.202
mv /var/log/long/ncku-csie-246-202-long.log /var/log/long/6-12/
python LogProcessor.py /var/log/long/101/5.log 140.117.101.5
mv /var/log/long/101/5.log /var/log/long/6-12/101-5.log
python LogProcessor.py /var/log/long/101/6.log 140.117.101.6
mv /var/log/long/101/6.log /var/log/long/6-12/101-6.log
python LogProcessor.py /var/log/long/101/7.log 140.117.101.7
mv /var/log/long/101/7.log /var/log/long/6-12/101-7.log
