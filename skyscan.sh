#!/bin/bash

# constants
WINEGARD_PORT=/dev/ttyUSB0

# constants
AZIMUTH_START=110
AZIMUTH_END=240
ELEVATION_START=18 
ELEVATION_END=58
STEP_ANGLE=1.0
OFFSET_ANGLE=0

# perform scan
python3 skyscan.py --comm_port $WINEGARD_PORT --azimuth_start $AZIMUTH_START --azimuth_end $AZIMUTH_END --elevation_start $ELEVATION_START --elevation_end $ELEVATION_END --step_angle $STEP_ANGLE --offset_angle $OFFSET_ANGLE
