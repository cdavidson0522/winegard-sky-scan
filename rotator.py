
# imports
import argparse
import socket

# imports
from library.winegard import Winegard

# constants
CMD_GET_POSITION = 'p'

# constants
CMD_SET_POSITION = 'P'
CMD_SET_POSITION_NUM_PARAMS = 3
CMD_SET_POSITION_AZIMUTH_INDEX = 1
CMD_SET_POSITION_ELEVATION_INDEX = 2

# constants
CMD_STOP = 'S'

# constants
RESP_SUCCESS = 0
RESP_FAILURE = 1

# constants
MAX_NUM_COMMAND_BYTES = 128

#
# This class provides the implementation to use a Winegard
# satellite dish as an antenna rotator in real time satellite
# tracking applications via the Hamlib rotctld protocol.
#
class Rotator:

	#
	# Constructor
	#
	# @param comm_port the winegard comm port
	# @param socket_host the socket host name
	# @param socket_port the socket port number
	# @param offset_angle the azimuth offset angle
	#
	def __init__(self, comm_port, socket_host, socket_port, offset_angle):

		# set socket parameters
		self.SOCKET_HOST = socket_host
		self.SOCKET_PORT = socket_port

		# initialize winegard
		self.winegard = Winegard(comm_port)
		self.winegard.set_offset_angle(offset_angle)

		# initialize socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#

	#
	# Performs connect
	#
	# This method connects to the Winegard satellite dish. It
	# then commands the Winegard satellite dish to enter the
	# motor menu in preparation for client motor commands.
	#
	# @return true if successful, false otherwise
	#
	def connect(self):

		# debug
		print('INFO: Performing connect')

		# initialize status
		status = False

		# attempt to connect winegard
		status0 = self.winegard.connect()

		# determine connection status
		if status0 == True:

			# perform commands
			status1 = self.winegard.quit_menu()
			status2 = self.winegard.enter_motor_menu()

			# update status
			status = status1 and status2

		else:

			# debug
			print('ERROR: Unable to connect to winegard')
		#

		# return the status
		return status
	#

	#
	# Performs listen
	#
	# This method will hold indefinitely while listening for
	# incoming connection requests. It will then establish a
	# connection with the client.
	#
	# @return true if successful, false otherwise
	#
	def listen(self):

		# debug
		print('INFO: Performing listen...')

		# initialize status
		status = False

		# determine if valid socket
		if self.socket != None:

			# bind socket
			self.socket.bind((self.SOCKET_HOST, self.SOCKET_PORT))

			# listen for incoming connections
			self.socket.listen()

			# accept client connection
			connection, address = self.socket.accept()

			# determine if valid connection
			if connection != None:

				# debug
				print(f'INFO: Connected with {address}')

				# set connection
				self.connection = connection

				# update status to indicate successful
				status = True
			#
		#

		# return the status
		return status
	#

	#
	# Performs processing
	#
	# This method will continuously process incoming command
	# data from the client until the STOP command is received.
	# This method parses the command data to determine the type
	# of command received in order to invoke the appropriate
	# process method, which will handle the command and generate
	# the expected response string. This method will then encode
	# the response string and send it to the client.
	#
	def process(self):

		# debug
		print('INFO: Processing commands')

		# obtain command data
		cmd_data = self.connection.recv(MAX_NUM_COMMAND_BYTES)

		# initialize the stop command state
		stop_cmd = False

		# loop while valid data received
		while cmd_data != None and stop_cmd == False:

			# obtain command values
			cmd = cmd_data.decode('utf-8')
			cmd_values = cmd.split()

			# initialize response
			response = f'RPRT {RESP_FAILURE}\n'

			# determine if valid number of values
			if len(cmd_values) > 0:

				# obtain the command type
				cmd_type = cmd_values[0]

				# determine the command type
				if cmd_type == CMD_GET_POSITION:

					# process command
					response = self.process_get_position_cmd(cmd_values)

				elif cmd_type == CMD_SET_POSITION:

					# process command
					response = self.process_set_position_cmd(cmd_values)

				elif cmd_type == CMD_STOP:

					# process command
					response = self.process_stop_cmd(cmd_values)

					# update stop command state
					stop_cmd = True

				else:

					# debug
					print(f'WARNING: Unknown command type {cmd_type}')
				#
			#

			# send response
			response_encoded = response.encode('utf-8')
			self.connection.sendall(response_encoded)

			# determine stop command state
			if stop_cmd == False:

				# obtain command data
				cmd_data = self.connection.recv(MAX_NUM_COMMAND_BYTES)
			#
		#
	#

	#
	# Processes the GET_POSITION command
	#
	# This method commands the Winegard satellite dish to obtain
	# the current azimuth/elevation angles. It then utilizes these
	# angles to build the client response string.
	#
	# @param cmd_values the command values
	#
	# @return the client response string
	#
	def process_get_position_cmd(self, cmd_values):

		# initialize response
		response = f'RPRT {RESP_FAILURE}\n'

		# obtain the winegard angles
		status, data = self.winegard.get_motor_angle_data()

		# determine if valid angle data
		if status == True:

			# obtain the angle data
			azimuth = data['azimuth_angle']
			elevation = data['elevation_angle']

			# update response
			response = f'{azimuth}\n{elevation}\n'

		else:

			# debug
			print('WARNING: Unable to get position')
		#

		# return the response
		return response
	#

	#
	# Processes the SET_POSITION command
	#
	# This method parses the commanded azimuth/elevation angles
	# and commands the Winegard satellite dish to move to this
	# position. It then utilizes the status of these commands
	# to build the client response string
	#
	# @param cmd_values the command values
	#
	# @return the client response string
	#
	def process_set_position_cmd(self, cmd_values):

		# initialize response
		response = f'RPRT {RESP_FAILURE}\n'

		# determine if valid number of parameters
		if len(cmd_values) == CMD_SET_POSITION_NUM_PARAMS:

			# obtain command parameters
			cmd_azimuth = cmd_values[CMD_SET_POSITION_AZIMUTH_INDEX]
			cmd_elevation = cmd_values[CMD_SET_POSITION_ELEVATION_INDEX]

			# cast command parameters
			cast_cmd_azimuth = float(cmd_azimuth)
			cast_cmd_elevation = float(cmd_elevation)

			# set the winegard angles
			status1 = self.winegard.set_azimuth_motor_angle(cast_cmd_azimuth)
			status2 = self.winegard.set_elevation_motor_angle(cast_cmd_elevation)

			# determine the status
			if status1 and status2:

				# update response
				response = f'RPRT {RESP_SUCCESS}\n'

			else:

				# debug
				print('WARNING: Unable to set position')
			#
		#

		# return the response
		return response
	#

	#
	# Processes the stop command
	#
	# This command prints a message to the console and builds
	# the client response string.
	#
	# @param cmd_values the command values
	#
	# @return the client response string
	#
	def process_stop_cmd(self, cmd_values):

		# initialize response
		response = f'RPRT 0\n'

		# debug
		print('INFO: Stop command received')

		# return the response
		return response
	#

	#
	# Performs cleanup
	#
	# This method disconnects from the Winegard satellite dish
	# and closes the client connection.
	#
	def cleanup(self):

		# debug
		print('INFO: Performing cleanup')

		# disconnect winegard
		self.winegard.disconnect()

		# determine if valid socket
		if self.socket != None:

			# close socket
			self.socket.close()
		#
	#
#

# MAIN

#
# Performs main logic
#
# TODO
#
# --------------------------------------------------------
#
if __name__ == "__main__":

	# initialize parser
	parser = argparse.ArgumentParser()
	parser.add_argument("--comm_port", action="store", required=True, help="The Winegard serial communication port")
	parser.add_argument("--socket_host", action="store", required=True, help="The socket host name")
	parser.add_argument("--socket_port", type=int, action="store", required=True, help="The socket port number")
	parser.add_argument("--offset_angle", type=int, default=0, action="store", required=False, help="The azimuth offset angle in degrees")

	# parse arguments
	args = parser.parse_args()

	# initialize rotator
	rotator = Rotator(args.comm_port, args.socket_host, args.socket_port, args.offset_angle)

	# connect to winegard
	status = rotator.connect()

	# determine connect status
	if status == True:

		# listen for client connections
		status = rotator.listen()

		# determine connection status
		if status == True:

			# process commands
			rotator.process()

			# perform cleanup
			rotator.cleanup()

			# debug
			print('INFO: Rotator complete!')

		else:

			# debug
			print('ERROR: Unable to connect to socket')

	else:

		# debug
		print('ERROR: Unable to connect to winegard')
#
