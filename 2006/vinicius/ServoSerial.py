#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function
import serial as PySerial
import Packet
import commands
import RPi.GPIO as GPIO
import time

"""
Serial interfaces (real and test) for communications with XL-320 servos.
"""

class DummySerial(object):
	"""
	A dummy interface to test with when not hooked up to real hardware. It does
	a decent job of mimicing the real thing.
	"""
	def __init__(self, port, printAll=False):
		self.port = port
		self.printAll = printAll

	@staticmethod
	def listSerialPorts():
		return ServoSerial.listSerialPorts()

	def open(self):
		pass

	def sendPkt(self, pkt):
		# print('serial write >>', pkt)
		return 0, None

	def readPkts(self, how_much=128):
		return [[0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C], [0xFF, 0xFF, 0xFD, 0x00, 0x03, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]]

	def read(self, how_much=128):
		return [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x04, 0x00, 0x55, 0x00, 0xA1, 0x0C]

	def write(self, data):
		# if self.printAll:
		# print('serial write >>', data)
		return len(data)

	def close(self):
		pass

	def flushInput(self):
		pass


class ServoSerial(object):
	"""
	A wrapper around pyserial to work with Dynamixel servos' half duplex
	interface. This requires extra hardware added to your normal full duplex
	serial port. Also, this uses the  RTS pin to toggle between Tx and Rx.

	All data that goes into this class via write() or returns from it via read()
	is a simple array of bytes (e.g., [1,34,234,1,0,24,67]). Internally, the class
	transforms those into a binary stream.

	This class also uses Packet to find and verify what is returned form read()
	is a valid packet.
	"""
	DD_WRITE = True       # data direction set to write
	DD_READ = False       # data direction set to read
	SLEEP_TIME = 0.00005    # sleep time between read/write
        DD_GPIO = 12          # direction pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Set GPIO mode
        tx = GPIO.HIGH           # Low for TX mode
        rx = GPIO.LOW          # High for RX mode
        directionPin = 23       # GPIO pin connected to Enable pins on buffer
        GPIO.setup(directionPin, GPIO.OUT)  # Configure pin for output
        disableDirPin = False

        def __init__(self, port, baud_rate=1000000):
		"""
		Constructor: sets up the serial port
		"""
                self.serial = PySerial.Serial(port=port,
                        baudrate = baud_rate,
                        parity=PySerial.PARITY_NONE,
                        stopbits=PySerial.STOPBITS_ONE,
                        bytesize=PySerial.EIGHTBITS,
                        timeout=0.001
                        )
#		self.dataDirection(self.rx)

	def __del__(self):
		"""
		Destructor: closes the serial port
		"""
		self.close()

        def dataDirection(self, d):
            ''' Set direction of data.  Either rx or tx'''
            if not self.disableDirPin:
                GPIO.output(self.directionPin, d)    # set the pin
		#print ('data direction set:' +str(d))
                #time.sleep(0.000050)   # sleep for 50uS to allow things to settle.  Decreases checksum errors
                #time.sleep(0.00050)

	@staticmethod
	def listSerialPorts():
		"""
		http://pyserial.readthedocs.io/en/latest/shortintro.html

		This calls the command line tool from pyserial to list the available
		serial ports.
		"""
		cmd = 'python -m serial.tools.list_ports'
		err, ret = commands.getstatusoutput(cmd)
		if not err:
			r = ret.split('\n')
			ret = []
			for line in r:
				if line.find('/dev/') >= 0:
					line = line.replace(' ', '')
					ret.append(line)
		return err, ret

	def open(self):
                self.serial.close()
		if self.serial.isOpen():
			raise Exception('SeroSerial::open() ... Oops, port is already open')
		self.serial.open()
                PySerial.time.sleep(self.SLEEP_TIME)
		if self.serial.isOpen():
			print('Opened {} @ {}'.format(self.serial.name, self.serial.baudrate))
		else:
			raise Exception('Could not open {}'.format(self.serial.port))

	@staticmethod
	def decode(buff):
		"""
		Transforms the raw buffer data read in into a list of bytes
		"""
		pp = list(map(ord, buff))
		#print('buffLen='+str(len(buff)))
                if 0 == len(pp) == 1:
			pp = []
		return pp

        def read(self, how_much=128):  # FIXME: 128 might be too much ... what is largest?
		"""
		This toggles the RTS pin and reads in data. It also converts the buffer
		back into a list of bytes and searches through the list to find valid
		packets of info. This only returns the first packet in the buffer.
		"""

                self.dataDirection(self.rx)

                PySerial.time.sleep(self.SLEEP_TIME)
		data = self.serial.read(how_much)
		#print('dataLen='+str(len(data)))
                data = self.decode(data)
                print('receiving:'+str(data))
                return data
		#ret = []
		#d = Packet.findPkt(data)

                #if len(d) > 0:  # FIXME: need a better way
		#	ret = d[0]  # should i take the last one ... most recent?
		#return ret  # what do i do if i find more?

#	def readPkts(self, how_much=128):  # FIXME: 128 might be too much ... what is largest?
#		"""
#		This toggles the RTS pin and reads in data. It also converts the buffer
#		back into a list of bytes and searches through the list to find valid
#		packets of info. If there is more than one packet, this returns an
#		array of valid packets.
#		"""
#
#               self.dataDirection(self.rx)
#               self.serial.flushOutput()
#		PySerial.time.sleep(self.SLEEP_TIME)
#		data = self.serial.read(how_much)
#		data = self.decode(data)
#
#               # return data
#		ret = Packet.findPkt(data)
#		return ret

	def write(self, pkt):
		"""
		This is a simple serial write command. It toggles the RTS pin and formats
		all of the data into bytes before it writes.
		"""

                self.dataDirection(self.tx)

                # prep data array for transmition
		pkt = bytearray(pkt)
		pkt = bytes(pkt)

		PySerial.time.sleep(self.SLEEP_TIME)
		#self.serial.flushInput()
		self.flushInput()
		time.sleep(0.00005)
                num = self.serial.write(pkt)
		time.sleep(0.0002)
#               self.serial.flush()
                self.dataDirection(self.rx)
#		PySerial.time.sleep(self.SLEEP_TIME)
#		self.read()
                return num

	def sendPkt(self, pkt, cnt=1):
		"""
		Sends a packet and waits for the status packet returned. If no return is given,
                then it resends the packet. If an error occurs, it also resends the packet.

		in:
			pkt - command packet to send to servo
			cnt - how many retries should this do? default = 1
		out:
			ans     - status packet returned
                        err_num - 0 if good, >0 if error
			err_str - None if good, otherwise a string
		"""
		err_num = 0
		err_str = None
		while (cnt > 0):  # changed this so it is no longer infinite retry
                        print ('writing:' + str(pkt))
            		self.write(pkt)         #send packet to servo
                        ans = self.read()       #get status packet returned
                        if ans:
				cnt = 0
				err_num, err_str = Packet.getErrorString(ans)
				if err_num:  # something went wrong, exit function
					print('Error[{}]: {}'.format(err_num, err_str))
					cnt = 0
				# else:
				# 	print('packet {}'.format(ans))
			else:
				cnt -= 1
				err_num = 0x01
				print('>> retry {} <<'.format(cnt))
		return ans, err_num, err_str

	def close(self):
		"""
		If the serial port is open, it closes it.
		"""
		if self.serial.isOpen():
			self.serial.close()

	def flushInput(self):
		"""
		Flush the input.
		"""
		self.serial.flushInput()
