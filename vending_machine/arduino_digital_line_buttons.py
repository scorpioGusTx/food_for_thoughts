#! /usr/bin/python
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
class button_controller:
	GET_BUTTONS   = "b"
	WE_SHALL_CONTINUE = {"1", "2"}
	WE_SHALL_CASH_OUT = {"3", "4"}
	BUTTON_1 = {"1"}
	BUTTON_2 = {"2"}
	BUTTON_3 = {"3"}
	BUTTON_4 = {"4"}
	BUTTON_COUNTDOWN_EXPIRED = {"X"}

	#
	# the column and row specifications are in the format of (bank, relay)
	#

	def __init__(self, serial_port):
		self.serial_connection = serial_port

	def are_pressed(self):
		out = []
                self.serial_connection.write(self.GET_BUTTONS)
		time.sleep(.2)
		while self.serial_connection.inWaiting() > 0:
			char = self.serial_connection.read(1)
			if char <> "\n":
				out += char

		return set(out)

	def wait_until_all_are_released(self):
		while len(self.are_pressed()) > 0:
			time.sleep(.1)
