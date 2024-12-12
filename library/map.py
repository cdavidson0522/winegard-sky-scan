
# includes
import numpy as np
import matplotlib.pyplot as plt

# constants
RSSI_MIN = 400
RSSI_MAX = 580

# constants
NUM_X_TICKS = 5
NUM_Y_TICKS = 3

#
# This class implements a heatmap to display satellite signal
# strength data in real-time as the map is constructed. Data
# points can also be overlayed on top of the satellite data.
#
class Map:

	#
	# Constructor
	#
	# @param azimuth_start the azimuth start angle
	# @param azimuth_end the azimuth end angle
	# @param elevation_start the elevation start angle
	# @param elevation_end the elevation end angle
	# @param step_angle the azimuth/elevation step angle
	#
	def __init__(self, azimuth_start, azimuth_end, elevation_start, elevation_end, step_angle):

		# set scan parameters
		self.AZIMUTH_START = azimuth_start
		self.AZIMUTH_END = azimuth_end
		self.ELEVATION_START = elevation_start
		self.ELEVATION_END = elevation_end
		self.STEP_ANGLE = float(step_angle)

		# DATA

		# determine map width/height
		width = int((self.AZIMUTH_END - self.AZIMUTH_START) / self.STEP_ANGLE)
		height = int((self.ELEVATION_END - self.ELEVATION_START) / self.STEP_ANGLE)

		# initialize data array
		self.data_array = np.empty((height+1, width+1))
		self.data_array.fill(RSSI_MAX)

		# PLOT

		# initialize extents
		extent = [self.AZIMUTH_START, self.AZIMUTH_END, self.ELEVATION_START, self.ELEVATION_END]

		# initialize plot
		self.plt_im = plt.imshow(self.data_array, cmap='CMRmap', vmin=RSSI_MIN, vmax=RSSI_MAX, extent=extent)
		plt.colorbar(pad=0.2, orientation='horizontal', location='bottom', label='RSSI')

		# set annotations
		plt.title('Sky Scan')
		plt.xlabel('Azimuth (deg)')
		plt.ylabel('Elevation (deg)')

		# increase the size of the plot
		plt_gcf = plt.gcf()
		plt_size_inches = plt_gcf.get_size_inches()
		plt_gcf.set_size_inches(plt_size_inches*1.5)

		# set x-axis ticks
		x_ticks = np.linspace(self.AZIMUTH_START, self.AZIMUTH_END, NUM_X_TICKS)
		plt.xticks(x_ticks)

		# set y-axis ticks
		y_ticks = np.linspace(self.ELEVATION_START, self.ELEVATION_END, NUM_Y_TICKS)
		plt.yticks(y_ticks)
	#

	#
	# Shows the map
	#
	def show(self):

		# show plot
		plt.ion()
		plt.show()

		# wait for plot to open
		plt.pause(1.0)
	#

	#
	# Sets the specified data point on the map
	#
	# This method will first determine the validity of the
	# supplied RSSI value. Valid RSSI values will be added to
	# the map. The redraw parameter will determine whether
	# execution is suspended to redraw the map. Invalid RSSI
	# values will be ignored.
	#
	# @param azimuth the azimuth angle
	# @param elevation the elevation angle
	# @param rssi the signal strength
	# @param redraw the redraw state
	#
	def set_data(self, azimuth, elevation, rssi, redraw=True):

		# determine if valid value
		if rssi > 0:

			# determine x position
			x_pos = int(round((azimuth - self.AZIMUTH_START) / self.STEP_ANGLE))

			# determine y position
			y_pos = int(round((self.ELEVATION_END - elevation) / self.STEP_ANGLE))

			# set data value
			self.data_array[y_pos, x_pos] = rssi

			# update plot data
			self.plt_im.set_data(self.data_array)

			# determine redraw state
			if redraw == True:

				# wait for plot to update
				plt.pause(0.001)
		#
	#

	#
	# Sets the specified point on the map
	#
	# This method will first determine the validity of the
	# supplied azimuth/elevation position. Points with valid
	# positions will be added to the map. The redraw parameter
	# will determine whether execution is suspended to redraw
	# the map. Points with invalid positions will be ignored.
	#
	# @param name the point name
	# @param azimuth the azimuth angle
	# @param elevation the elevation angle
	# @param redraw the redraw state
	#
	def set_point(self, name, azimuth, elevation, redraw=True):

		# determine position validity
		valid1 = azimuth >= self.AZIMUTH_START and azimuth <= self.AZIMUTH_END
		valid2 = elevation >= self.ELEVATION_START and elevation <= self.ELEVATION_END

		# determine if valid position
		if valid1 and valid2:

			# add point to plot
			plt.plot(azimuth, elevation, marker='o')
			plt.annotate(text=name, xy=(azimuth, elevation), fontsize=8, weight='light')

			# determine redraw state
			if redraw == True:

				# wait for plot to update
				plt.pause(0.001)
			#
		#
	#

	#
	# Saves the map to the specified file path
	#
	# @param file_path the file path
	#
	def save(self, file_path):

		# save plot
		plt.savefig(file_path)
	#
#
