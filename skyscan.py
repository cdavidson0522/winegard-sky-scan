
# imports
import os
import argparse
import time
import decimal

# imports
from datetime import datetime

# imports
from library.map import Map
from library.winegard import Winegard

# constants
START_DELAY = 4.0
ANGLE_DELAY = 0.2
SWEEP_DELAY = 1.0

# constants
RSSI_INVALID = -1

# constants
OUTPUT_DIR = 'scan_data'

#
# This class provides the implementation to perform a sky scan
# with a Winegard satellite dish. This sky scan will collect
# signal strength data at each elevation/azimuth position and
# plot it on a heatmap in real time. It will also save this data
# to an output file.
#
class SkyScan:

	#
	# Constructor
	#
	# @param comm_port the winegard comm port
	# @param azimuth_start the azimuth start angle
	# @param azimuth_end the azimuth end angle
	# @param elevation_start the elevation start angle
	# @param elevation_end the elevation end angle
	# @param step_angle the step angle
	# @param offset_angle the azimuth offset angle
	#
	def __init__(self, comm_port, azimuth_start, azimuth_end, elevation_start, elevation_end, step_angle, offset_angle):

		# set scan parameters
		self.AZIMUTH_START = azimuth_start
		self.AZIMUTH_END = azimuth_end
		self.ELEVATION_START = elevation_start
		self.ELEVATION_END = elevation_end
		self.STEP_ANGLE = step_angle

		# determine start date/time
		now = datetime.now()
		self.start_time = now.strftime("%Y_%m_%d_%H_%M_%S")

		# initialize winegard
		self.winegard = Winegard(comm_port)
		self.winegard.set_offset_angle(offset_angle)

		# initialize map
		self.map = Map(self.AZIMUTH_START, self.AZIMUTH_END, self.ELEVATION_START, self.ELEVATION_END, self.STEP_ANGLE)
	#

	#
	# Performs setup
	#
	# This method opens the data output file and connects to the
	# Winegard satellite dish. It then commands the Winegard
	# satellite dish to enable the LNA and move to the starting
	# azimuth/elevation position.
	#
	# @return true if successful, false otherwise
	#
	def setup(self):

		# debug
		print('INFO: Performing setup')

		# initialize status
		status = False

		# create output directory
		os.makedirs(OUTPUT_DIR, exist_ok=True)

		# initialize file path
		file_name = f'{self.start_time}.txt'
		file_path = os.path.join(OUTPUT_DIR, file_name)

		# open output file
		self.output_file = open(file_path, 'w')

		# determine if valid file
		if self.output_file != None:

			# attempt to connect winegard
			status = self.winegard.connect()

			# determine connection status
			if status == True:

				# perform commands
				status1 = self.winegard.quit_menu()
				status2 = self.winegard.enter_dvb_menu()
				status3 = self.winegard.enable_dvb_lna()
				status4 = self.winegard.quit_dvb_menu()
				status5 = self.winegard.enter_motor_menu()
				status6 = self.winegard.set_azimuth_motor_angle(self.AZIMUTH_START)
				status7 = self.winegard.set_elevation_motor_angle(self.ELEVATION_START)

				# wait for motor movement to complete
				time.sleep(START_DELAY)

				# update status
				status = status1 and status2 and status3 and status4 and status5 and status6 and status7

			else:

				# debug
				print('ERROR: Unable to connect to winegard')

		else:

			# debug
			print('ERROR: Unable to open output file')
		#

		# return the status
		return status
	#

	#
	# Performs show
	#
	# This method shows the map such that it can be populated in
	# real time with subsequent scan data
	#
	def show_map(self):

		# debug
		print('INFO: Performing show')

		# show the map
		self.map.show()
	#

	#
	# Performs scan
	#
	# This method commands the Winegard satellite dish to each
	# azimuth/elevation position and captures the average RSSI
	# signal strength. It then updates the corresponding point
	# on the map and writes the values to the data output file.
	#
	def scan(self):

		# debug
		print('INFO: Performing scan...')

		# loop through azimuth angles
		for azimuth in self.drange(self.AZIMUTH_START, self.AZIMUTH_END, self.STEP_ANGLE):

			# position azimuth motor
			self.winegard.set_azimuth_motor_angle(azimuth)

			# loop through elevation angles
			for elevation in self.drange(self.ELEVATION_START, self.ELEVATION_END, self.STEP_ANGLE):

				# position elevation motor
				self.winegard.set_elevation_motor_angle(elevation)

				# wait for motor movement to complete
				time.sleep(ANGLE_DELAY)

				# open DVB menu
				self.winegard.quit_motor_menu()
				self.winegard.enter_dvb_menu()

				# initialize values
				rssi = RSSI_INVALID

				# obtain RSSI data
				status, data = self.winegard.get_dvb_rssi_data()

				# determine if valid RSSI data
				if status == True:

					# obtain RSSI data values
					rssi = data['rssi_avg']
				#

				# debug
				print(f'INFO: Az={azimuth}, El={elevation}, RSSI={rssi}')

				# update map data
				self.map.set_data(azimuth, elevation, rssi)

				# write to file
				self.output_file.write(f'{azimuth} {elevation} {rssi}\n')

				# open motor menu
				self.winegard.quit_dvb_menu()
				self.winegard.enter_motor_menu()
			#

			# flush the file data
			self.output_file.flush()

			# position elevation motor
			self.winegard.set_elevation_motor_angle(self.ELEVATION_START)

			# wait for motor movement to complete
			time.sleep(SWEEP_DELAY)
		#

		# open main menu
		self.winegard.quit_menu()
	#

	#
	# Performs save
	#
	# This method saves an image of the map to the output
	# directory.
	#
	def save_map(self):

		# debug
		print('INFO: Performing save')

		# initialize file path
		file_name = f'{self.start_time}.png'
		file_path = os.path.join(OUTPUT_DIR, file_name)

		# save the map
		self.map.save(file_path)
	#

	#
	# Performs cleanup
	#
	# This method closes the data output file and disconnects
	# from the Winegard satellite dish.
	#
	def cleanup(self):

		# debug
		print('INFO: Performing cleanup')

		# close output file
		self.output_file.close()

		# disconnect winegard
		self.winegard.disconnect()
	#

	# HELPER

	#
	# Generates list of decimal numbers
	#
	# @param x the list start value
	# @param y the list end value
	# @param jump the jump value
	#
	# @return the list of decimal numbers
	#
	def drange(self, x, y, jump):
		while x <= y:
			yield float(x)
			x += decimal.Decimal(jump)
		#
	#
#

# MAIN

#
# Performs main logic
#
# This method parses the supplied arguments, connects to the
# Winegard satellite dish, displays the heatmap, and performs
# the scan over the region of interest. Once the scan is
# complete, the scan data is saved and the connection with the
# Winegard satellite dish is closed.
#
if __name__ == "__main__":

	# initialize parser
	parser = argparse.ArgumentParser()
	parser.add_argument("--comm_port", action="store", required=True, help="The Winegard serial communication port")
	parser.add_argument("--azimuth_start", type=int, action="store", required=True, help="The azimuth start angle in degrees")
	parser.add_argument("--azimuth_end", type=int, action="store", required=True, help="The azimuth end angle in degrees")
	parser.add_argument("--elevation_start", type=int, action="store", required=True, help="The elevation start angle in degrees")
	parser.add_argument("--elevation_end", type=int, action="store", required=True, help="The elevation end angle in degrees")
	parser.add_argument("--step_angle", type=float, action="store", required=True, help="The step angle in degrees")
	parser.add_argument("--offset_angle", type=int, default=0, action="store", required=False, help="The azimuth offset angle in degrees")

	# parse arguments
	args = parser.parse_args()

	# initialize sky scan
	skyscan = SkyScan(args.comm_port, args.azimuth_start, args.azimuth_end, args.elevation_start, args.elevation_end, args.step_angle, args.offset_angle)

	# perform setup
	status = skyscan.setup()

	# determine setup status
	if status == True:

		# show the map
		skyscan.show_map()

		# perform scan
		skyscan.scan()

		# save the map
		skyscan.save_map()

		# perform cleanup
		skyscan.cleanup()

		# debug
		print('INFO: Scan complete!')

		# wait for exit
		input('Press any key to exit')

	else:

		# debug
		print('ERROR: An error occurred during setup')
	#
#
