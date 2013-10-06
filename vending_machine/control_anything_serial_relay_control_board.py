#! /usr/bin/python
import time
import serial
import socket



# configure the serial connections (the parameters differs on the device you are connecting to)
class dispensor:
	#
	# the column and row specifications are in the format of (bank, relay)
	#

	rows = ((2, 3), (2, 4), (2, 1), (2, 2), (2,5), (2,0), (2, 6), (2, 7))

# is working
	columns = ((1, 5), (1,3), (1, 2), (1, 1))
# (1, 3), (1, 4), (1, 5))

	columns_per_row = (4, 4, 4, 4, 4, 8)
	column_to_dispense = (0, 0, 0, 0, 0, 0)

	def __init__(self):
		if socket.gethostname() == "pegasus":
			device_name = "/dev/ttyAMA0"
			device_name = "/dev/ttyUSB0"
		else:
			device_name = "/dev/ttyS0"

		self.serial_connection = serial.Serial(
			port=device_name,
#			baudrate=115200,
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)

		self.serial_connection.open()
		self.serial_connection.isOpen()

		self.send(chr(254) + chr(248)) # enable all devices
		time.sleep(.01)
		# self.send(chr(254) + chr(27)) # activate report mode
		self.send(chr(254) + chr(28)) # deactivate report mode
		time.sleep(.01)
		self.send(chr(254) + chr(129) + chr(0))
		time.sleep(.01)

	def send(self, message):
		self.serial_connection.write(message)

	def relay_on(self, relay_specification):
		bank = relay_specification[0]
		relay = relay_specification[1]

		self.send(chr(254) + chr(108 + relay) + chr(bank))
		time.sleep(.01)

	def relay_off(self, relay_specification):
		bank = relay_specification[0]
		relay = relay_specification[1]

		self.send(chr(254) + chr(100 + relay) + chr(bank))
		time.sleep(.01)

	def dispense(self, column, row):
		self.relay_on(self.rows[row])
		self.relay_on(self.columns[column])

		time.sleep(7)

		self.relay_off(self.rows[row])
		self.relay_off(self.columns[column])

	def dispense_candy(self, level):
		self.column_to_dispense[level] += 1
		if not(self.column_to_dispense[level] < self.columns_per_row[level]):
			self.column_to_dispense[level] = 0

		self.dispense(column_to_dispense[level], 7 - level)

class leds:
	ANSWER_WRONG_MODE   = "w"
	ANSWER_CORRECT_MODE = "c"
	CHASE_MODE          = "a"
	COUNTDOWN_MODE      = "d"
	FLASH_MODE          = "f"

	def __init__(self):
		self.serial_connection = serial.Serial("/dev/ttyACM0")

		self.serial_connection.open()
		self.serial_connection.isOpen()

	def send(self, message):
		self.serial_connection.write(message)
