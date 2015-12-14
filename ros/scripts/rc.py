#!/usr/bin/env python

import sys, rospy, mavros
from mavros_msgs.msg import OverrideRCIn

def init():
	mavros.set_namespace('/mavros')
	rospy.init_node("time", anonymous=True)

	return rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)

def send(publisher, roll, pitch, throttle, yaw):
	min_val = 1000;
	max_val = 2000;

	if len( filter( lambda x: x < min_val or x > max_val, [roll, pitch, throttle, yaw] ) ) > 0:
		print 'Values must be between %d and %d' % (min_val, max_val)
		return False

	msg = OverrideRCIn()
	msg.channels[0] = roll
	msg.channels[1] = pitch
	msg.channels[2] = throttle
	msg.channels[3] = yaw
	msg.channels[4] = 1100
	msg.channels[5] = 1100
	msg.channels[6] = 1100
	msg.channels[7] = 1100

	print publisher.publish(msg)

	return True

if __name__ == '__main__':
	publisher = init()
	
	while True:
		c = raw_input("Enter roll, pitch, throttle and yaw: ")
		if c == "exit":
			break
		try:
			roll, pitch, throttle, yaw = map(int, c.split())
			if send(publisher, roll, pitch, throttle, yaw):
				print 'Successfully sent'
			else:
				print 'Failed to send'
		except:
			print 'Invalid input'
