#!/bin/bash

# constants
WINEGARD_PORT=/dev/ttyUSB0

# constants
SOCKET_HOST="127.0.0.1"
SOCKET_PORT=4533
OFFSET_ANGLE=0

# perform rotator
python3 rotator.py --comm_port $WINEGARD_PORT --socket_host $SOCKET_HOST --socket_port $SOCKET_PORT --offset_angle $OFFSET_ANGLE
