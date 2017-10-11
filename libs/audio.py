#!/usr/bin/env python
import os
import os.path
import usb.core
import time
import sys
import logging
from subprocess import call


def connect(vendor,product):
	dev = usb.core.find(idVendor=int(vendor, 16), idProduct=int(product, 16))
	try:
		mesg = dev.ctrl_transfer(0xc0, 51, 0, 0, 2)
		# here we should check if it returned version 2
		print 'received mesg of %s'.format(mesg)
		time.sleep(1)
		# requesting audio
		dev.ctrl_transfer(0x40, 0x3a, 1, 0, "")
		print 'requested audio'

		# putting device in accessory mode
		dev.ctrl_transfer(0x40, 53, 0, 0, "")
		print 'put into accessory mode'
	except:
		dev = usb.core.find(idVendor=int('18d1', 16), idProduct=int('2d02', 16))
		mesg = dev.ctrl_transfer(0xc0, 51, 0, 0, 2)
		# here we should check if it returned version 2
		print 'received mesg of %s'.format(mesg)
		time.sleep(1)
		# requesting audio
		dev.ctrl_transfer(0x40, 0x3a, 1, 0, "")
		print 'requested audio'

		# putting device in accessory mode
		dev.ctrl_transfer(0x40, 53, 0, 0, "")
		print 'put into accessory mode'
	print 'finished script'
	startaudio()
	
def startaudio():
	print 'loading audio'
	time.sleep(3)
	call(('pactl','set-default-source','alsa_input.usb-motorola_XT1565_ZY2227GPNS-00.analog-stereo'))
	

