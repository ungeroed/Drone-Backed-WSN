import serial, time, sys

class DroneArduino():

	def __init__(self, device):
		self.arduino = serial.Serial(device, 9600, timeout=.2)
		time.sleep(2.)

	def __execute_command(self, cmd):
		attempts = 10
		for i in range(attempts):
		  try:
			  self.arduino.write(cmd)
			  return self.arduino.readline()[:-2]
		  except OSError:
			  if i == attempts - 1:
				  return 'OSError'
		  except serial.SerialException:
			  if i == attempts - 1:
				return 'SerialException'

	def ping_radio_ack(self):
		return self.__execute_command('a')

	def ping_radio_echo(self):
		return self.__execute_command('e')

	def get_distance(self):
		return self.__execute_command('d')

if __name__ == '__main__':
	arduino = DroneArduino('/dev/ttyUSB0')

	# Get input parameters
	#action = sys.argv[1]
	#count = int(sys.argv[2])
	#distance = sys.argv[3]

	count = int(sys.argv[1])
	distance = sys.argv[2]
	
	## Select the action
	#if action == 'ping_radio_ack':
	#	fun = arduino.ping_radio_ack
	#elif action == 'ping_radio_echo':
	#	fun = arduino.ping_radio_echo
	#elif action == 'get_distance':
	#	fun = arduino.get_distance
	#else:
	#	raise ValueError('invalid action')

	fun = arduino.ping_radio_ack
		

	# Time the action and print the results
	#print 'distance', action, 'time'
	for i in range(count):
		t = time.time()
		print distance, fun(), (time.time() - t)

