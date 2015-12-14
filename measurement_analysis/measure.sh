#!/bin/bash
DISTANCE=$1
#python drone_arduino.py ping_radio_ack 1000 $DISTANCE >> ../measurements/radio_ack.csv
#python drone_arduino.py ping_radio_echo 1000 $DISTANCE >> ../measurements/radio_echo.csv

python drone_arduino.py 1000 $DISTANCE > long_ack_$DISTANCE.csv
echo "done"
