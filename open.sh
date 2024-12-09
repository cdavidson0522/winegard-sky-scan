#!/bin/bash

# constants
SCAN_FILE=example/scan_data.txt
SATELLITE_FILE=example/satellite_data.csv

# open scan file
python3 open.py --scan_file $SCAN_FILE --satellite_file $SATELLITE_FILE
