
# imports
import serial
import time
import re

# constants
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = 15

# constants
END_CHARACTER = 62 # '>'

# constants
AZIMUTH_MOTOR_INDEX = 0
ELEVATION_MOTOR_INDEX = 1

# constants
LNA_MODE_ODU = 'odu'

# constants
RSSI_ITERATIONS = 10

#
# This class provides the ability to connect to a Winegard
# satellite dish to enable the LNA, position the dish to the
# specified azimuth/elevation position, and capture the RSSI
# signal strength.
#
class Winegard:

	#
	# Constructor
	#
	# @param serial_port the Winegard serial port
	#
	def __init__(self, serial_port):
		
		# set parameters
		self.SERIAL_PORT = serial_port
		self.OFFSET_ANGLE = 0
	#

	#
	# Sets the azimuth offset angle
	#
	# @param offset_angle the azimuth offset angle
	#
	def set_offset_angle(self, offset_angle):

		# set parameters
		self.OFFSET_ANGLE = offset_angle
	#

	# CONNECTION

	#
	# Performs connect
	#
	# This method attempts to open a serial connection to the
	# Winegard satellite dish.
	#
	# @return true if successful, false otherwise
	#
	def connect(self):

		# initialize status
		status = False

		# open serial port
		self.ser = serial.Serial(port=self.SERIAL_PORT, baudrate=SERIAL_BAUD, timeout=SERIAL_TIMEOUT)

		# determine if valid serial
		if self.ser != None:

			# update status to indicate successful
			status = True
		#

		# return the status
		return status
	#

	#
	# Performs disconnect
	#
	# This method disconnects from the Winegard satellite dish.
	#
	# @return true if successful, false otherwise
	#
	def disconnect(self):

		# initialize status
		status = False

		# determine if valid serial
		if self.ser != None:

			# close the serial port
			self.ser.close()

			# update status to indicate successful
			status = True
		#

		# return the status
		return status
	#

	# MAIN MENU

	#
	# Quits the menu
	#
	# This method sends the command to exit the current menu.
	#
	# @return true if successful, false otherwise
	#
	def quit_menu(self):

		# initialize command
		command = 'q\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	# MOTOR MENU

	#
	# Enters the motor menu
	#
	# This method attempts to enter the motor menu. This command
	# is only valid on the main menu.
	#
	# @return true if successful, false otherwise
	#
	def enter_motor_menu(self):

		# initialize command
		command = 'mot\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Homes the azimuth motor
	#
	# This method attempts to home the azimuth motor. This command
	# is only valid on the motor menu.
	#
	# @return true if successful, false otherwise
	#
	def home_azimuth_motor(self):

		# initialize command
		command = f'h {AZIMUTH_MOTOR_INDEX}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Homes the elevation motor
	#
	# This method attempts to home the elevation motor. This command
	# is only valid on the motor menu.
	#
	# @return true if successful, false otherwise
	#
	def home_elevation_motor(self):

		# initialize command
		command = f'h {ELEVATION_MOTOR_INDEX}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Determines the motor angle data
	#
	# This method attempts to determine the current motor
	# angles. This command is only valid on the motor menu.
	#
	# @return true if successful, false otherwise
	# @return the motor angle data if successful
	#
	def get_motor_angle_data(self):

		# initialize status
		status = False

		# initialize response data
		resp_data = {}

		# initialize command
		command = 'a\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# determine if valid status
		if cmd_status == True:

			# parse data from response
			results = re.findall(r'\d+\.\d+', cmd_response)

			# determine if valid results
			if len(results) == 2:

				# obtain position data
				azimuth_angle = float(results[0])
				elevation_angle = float(results[1])

				# determine adjusted angle
				azimuth_angle_adjusted = (azimuth_angle - self.OFFSET_ANGLE) % 360

				# set position data values
				resp_data['azimuth_angle'] = azimuth_angle_adjusted
				resp_data['elevation_angle'] = elevation_angle

				# update status to indicate successful
				status = True
			#
		#

		# return the status and response data
		return status, resp_data
	#

	#
	# Sets the azimuth motor angle
	#
	# This method attempts to set the azimuth motor angle. This
	# command is only valid on the motor menu. The valid azimuth
	# angles are [0-359].
	#
	# @param angle the desired azimuth angle
	#
	# @return true if successful, false otherwise
	# 
	def set_azimuth_motor_angle(self, angle):

		# determine adjusted angle
		angle_adjusted = (angle + self.OFFSET_ANGLE) % 360
		
		# initialize command
		command = f'a {AZIMUTH_MOTOR_INDEX} {angle_adjusted}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Sets the elevation motor angle
	#
	# This method attempts to set the elevation motor angle. This
	# command is only valid on the motor menu. The valid elevation
	# angles are [18,65].
	#
	# @param angle the desired elevation angle
	#
	# @return true if successful, false otherwise
	#
	def set_elevation_motor_angle(self, angle):

		# initialize command
		command = f'a {ELEVATION_MOTOR_INDEX} {angle}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Quits the motor menu
	#
	# This method attempts to quit the motor menu. This command
	# is only valid on the motor menu.
	#
	# @return true if successful, false otherwise
	#
	def quit_motor_menu(self):

		# initialize command
		command = 'q\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	# DVB MENU

	#
	# Enters the DVB menu
	#
	# This method attempts to enter the DVB menu. This command
	# is only valid on the main menu.
	#
	# @return true if successful, false otherwise
	#
	def enter_dvb_menu(self):

		# initialize command
		command = 'dvb\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Enables the DVB LNA
	#
	# This method attempts to enable the LNA in ODU mode. This
	# command is only valid on the DVB menu.
	#
	# @return true if successful, false otherwise 
	#
	def enable_dvb_lna(self):

		# initialize command
		command = f'lnbdc {LNA_MODE_ODU}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	#
	# Determines the DVB RSSI
	#
	# This method attempts to obtain the RSSI signal strength
	# by averaging the specified number of samples. This command
	# is only valid on the DVB menu.
	#
	# @param iterations the number of iterations
	#
	# @return true if successful, false otherwise
	# @return the DVB RSSI data if successful
	#
	def get_dvb_rssi_data(self, iterations=RSSI_ITERATIONS):

		# initialize status
		status = False

		# initialize response data
		resp_data = {}

		# initialize command
		command = f'rssi {iterations}\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# determine if valid status
		if cmd_status == True:

			# parse data from response
			results = re.findall(r'\d+', cmd_response)

			# determine if valid results
			if len(results) == 6:

				# obtain rssi data values
				resp_data['rssi_reads'] = int(results[3])
				resp_data['rssi_avg'] = int(results[4])
				resp_data['rssi_cur'] = int(results[5])

				# update status to indicate successful
				status = True
			#
		#

		# return the status and response data
		return status, resp_data
	#

	#
	# Quits the DVB menu
	#
	# This method attempts to quit the DVB menu. This command
	# is only valid on the DVB menu.
	#
	# @return true if successful, false otherwise
	#
	def quit_dvb_menu(self):

		# initialize command
		command = 'q\r'

		# send command
		cmd_status, cmd_response = self.send(command)

		# return the status
		return cmd_status
	#

	# HELPER

	#
	# Sends the supplied command
	#
	# This method attempts to send the supplied command and
	# capture the response data. This method will timeout if
	# the expected end character is not received.
	#
	# @param cmd_string the command to send
	#
	# @return true if successful, false otherwise
	# @return the response string if successful
	#
	def send(self, cmd_string):

		# initialize status
		status = False

		# initialize response
		response = []

		# determine if valid serial
		if self.ser != None:

			# obtain command bytes
			cmd_bytes = cmd_string.encode('utf-8')

			# write serial data
			self.ser.write(cmd_bytes)

			# initialize response data
			resp_data = []
			resp_timeout = False

			# read until end character is encountered
			while END_CHARACTER not in resp_data and resp_timeout == False:

				# read one byte of data
				# this can timeout and return 0 bytes of data
				resp_bytes = self.ser.read(size=1)

				# determine number of bytes received
				if len(resp_bytes) > 0:

					# append bytes to response
					resp_data += resp_bytes

				else:

					# serial timeout occurred
					resp_timeout = True
				#
			#

			# determine whether timeout occurred
			if resp_timeout == False:

				# convert response data to string
				byte_array = bytearray(resp_data)
				response = byte_array.decode('utf-8')

				# update status to indicate successful
				status = True
			#

			# wait before allowing next command
			time.sleep(0.001)

			# return the status and response string
			return status, response
		#
	#
#
