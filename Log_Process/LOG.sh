#!/bin/bash
python LogProcessor.py /var/log/long/1.log 140.117.205.1
mv /var/log/long/1.log /var/log/long/6-17/
python LogProcessor.py /var/log/long/ncku-csie-246-202-long.log 140.116.246.202
mv /var/log/long/ncku-csie-246-202-long.log /var/log/long/6-17/
python LogProcessor.py /var/log/long/101/5.log 140.117.101.5
mv /var/log/long/101/5.log /var/log/long/6-17/101-5.log
python LogProcessor.py /var/log/long/101/6.log 140.117.101.6
mv /var/log/long/101/6.log /var/log/long/6-17/101-6.log
python LogProcessor.py /var/log/long/101/7.log 140.117.101.7
mv /var/log/long/101/7.log /var/log/long/6-17/101-7.log
