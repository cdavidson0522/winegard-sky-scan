
# imports
import argparse
import time

# imports
from library.winegard import Winegard

# constants
START_DELAY = 4.0
SOUTH_DEGREES = 180

# PARSE ARGS

# initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("--comm_port", action="store", required=True, help="The Winegard serial communication port")

# parse arguments
args = parser.parse_args()

# CONNECT

# initialize winegard
winegard = Winegard(args.comm_port)

# attempt to connect winegard
status0 = winegard.connect()

# determine connection status
if status0 == True:

	# MESSAGE

	# debug
	print('INFO: Winegard will spin; hold cables')

	# wait for continue
	input('Press any key to continue')

	# HOMING

	# perform commands
	status1 = winegard.quit_menu()
	status2 = winegard.enter_motor_menu()
	status3 = winegard.home_azimuth_motor()
	status4 = winegard.home_elevation_motor()
	status5 = winegard.set_azimuth_motor_angle(SOUTH_DEGREES)
	status6 = winegard.quit_motor_menu()

	# wait for motor movement to complete
	time.sleep(START_DELAY)

	# determine status
	if status1 and status2 and status3 and status4 and status5 and status6:

		# debug
		print('INFO: Homing complete!')

	else:

		# debug
		print('ERROR: An error occurred during homing')
	#

else:

	# debug
	print('ERROR: Unable to connect to winegard')
#
