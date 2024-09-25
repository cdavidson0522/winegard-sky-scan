#!/bin/bash

# constants
WINEGARD_PORT=/dev/ttyUSB0

# perform homing
python3 home.py --comm_port $WINEGARD_PORT 
