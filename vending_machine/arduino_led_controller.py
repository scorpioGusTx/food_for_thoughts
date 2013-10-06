#! /usr/bin/python
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
class controller:
	ATTRACT_MODE        = "a"
	COUNTDOWN_MODE      = "d"
	ANSWER_CORRECT_MODE = "c"
	ANSWER_WRONG_MODE   = "w"

	#
	# the column and row specifications are in the format of (bank, relay)
	#

	def __init__(self):
		device_name = "/dev/ttyACM0"

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

	def send(self, message):
		print(message)
		self.serial_connection.write(message)

	def attract(self):
		self.send(self.ATTRACT_MODE)

	def countdown(self):
		self.send(self.COUNTDOWN_MODE)

	def correct(self):
		self.send(self.ANSWER_CORRECT_MODE)

	def wrong(self):
		self.send(self.ANSWER_WRONG_MODE)


