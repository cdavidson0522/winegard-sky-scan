
# imports
import os
import argparse
import csv

# imports
from library.map import Map

# constants
SCAN_DATA_NUM_VALUES = 3
SCAN_DATA_AZIMUTH_INDEX = 0
SCAN_DATA_ELEVATION_INDEX = 1
SCAN_DATA_RSSI_INDEX = 2

# constants
SATELLITE_DATA_NUM_VALUES = 3
SATELLITE_DATA_NAME_INDEX = 0
SATELLITE_DATA_AZIMUTH_INDEX = 1
SATELLITE_DATA_ELEVATION_INDEX = 2

# constants
MIN_NUM_SCAN_DATA_ENTRIES = 2

# constants
ANIMATE_DRAWING_MAP = False

# PARSE ARGS

# initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("--scan_file", action="store", required=True, help="The scan data file path")
parser.add_argument("--satellite_file", action="store", required=False, help="The satellite data file path")

# parse arguments
args = parser.parse_args()

# READ SCAN DATA

# initialize data
scan_data = []

# determine if file exists
if os.path.isfile(args.scan_file) == True:

	# debug
	print('INFO: Reading scan data')

	# open input file
	file = open(args.scan_file, 'r')

	# loop through file lines
	for line in file:

		# split line into values
		line_data = line.split()

		# determine if valid number of values
		if len(line_data) == SCAN_DATA_NUM_VALUES:

			# parse line data
			azimuth = line_data[SCAN_DATA_AZIMUTH_INDEX]
			elevation = line_data[SCAN_DATA_ELEVATION_INDEX]
			rssi = line_data[SCAN_DATA_RSSI_INDEX]

			# initialize data entry
			data_entry = {	'azimuth': float(azimuth),
							'elevation': float(elevation),
							'rssi': float(rssi) }

			# append scan data
			scan_data.append(data_entry)

		else:

			# debug
			print(f'WARNING: Invalid line ignored: {line}')
	#

	# close input file
	file.close()

else:

	# debug
	print('ERROR: The specified scan data file doesn\'t exist')
#

# READ SATELLITE DATA

# initialize data
satellite_data = []

# determine if satellite data provided
if args.satellite_file != None:

	# determine if file exists
	if os.path.isfile(args.satellite_file) == True:

		# debug
		print('INFO: Reading satellite data')

		# open input file
		csv_file = open(args.satellite_file, newline='')
		csv_reader = csv.reader(csv_file, delimiter=',')

		# loop through each row of satellite data
		for row_data in csv_reader:

			# determine if valid number of values
			if len(row_data) == SATELLITE_DATA_NUM_VALUES:

				# parse row data
				name = row_data[SATELLITE_DATA_NAME_INDEX]
				azimuth = row_data[SATELLITE_DATA_AZIMUTH_INDEX]
				elevation = row_data[SATELLITE_DATA_ELEVATION_INDEX]

				# initialize data entry
				data_entry = {	'name': name,
								'azimuth': float(azimuth),
								'elevation': float(elevation) }

				# append satellite data
				satellite_data.append(data_entry)

			else:

				# debug
				print(f'WARNING: Invalid row ignored: {row_data}')
			#

		# close input file
		csv_file.close()

	else:

		# debug
		print('ERROR: The specified satellite data file doesn\'t exist')
	#
#

# DRAW MAP

# determine if valid number of entries
if len(scan_data) >= MIN_NUM_SCAN_DATA_ENTRIES:

	# debug
	print('INFO: Determining scan parameters')

	# determine azimuth start/end
	azimuth_start = min(d['azimuth'] for d in scan_data)
	azimuth_end = max(d['azimuth'] for d in scan_data)

	# determine elevation start/end
	elevation_start = min(d['elevation'] for d in scan_data)
	elevation_end = max(d['elevation'] for d in scan_data)

	# determine step angle
	step_angle_azimuth = scan_data[1]['azimuth'] - scan_data[0]['azimuth']
	step_angle_elevation = scan_data[1]['elevation'] - scan_data[0]['elevation']
	step_angle = max([step_angle_azimuth, step_angle_elevation])

	# debug
	print('INFO: Drawing map...')

	# initialize map
	map = Map(azimuth_start, azimuth_end, elevation_start, elevation_end, step_angle)
	map.show()

	# loop through scan data
	for data_entry in scan_data:

		# obtain data values
		azimuth = data_entry['azimuth']
		elevation = data_entry['elevation']
		rssi = data_entry['rssi']

		# update map data
		map.set_data(azimuth, elevation, rssi, redraw=ANIMATE_DRAWING_MAP)
	#

	# loop through satellite data
	for data_entry in satellite_data:

		# obtain data values
		name = data_entry['name']
		azimuth = data_entry['azimuth']
		elevation = data_entry['elevation']

		# update map data
		map.set_point(name, azimuth, elevation, redraw=ANIMATE_DRAWING_MAP)
	#

	# debug
	print('INFO: Drawing complete!')

else:

	# debug
	print('ERROR: Invalid number of entries')
#

# wait for exit
input('Press any key to exit') 
