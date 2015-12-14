#!/usr/bin/env python

import time, math
import rospy
import mavros
import readline

from mavros import command, setpoint as sp
from mavros.utils import *
from mavros.param import param_set
from mavros_msgs.msg import State, OverrideRCIn
from mavros_msgs.srv import SetMode, ParamSet

from tf.transformations import quaternion_from_euler
from sensor_msgs.msg import NavSatFix

def init():
	#rospy.init_node('mavsys', anonymous=True)
	#rospy.init_node('mavsafety', anonymous=True)
	#rospy.init_node('mavsetp', anonymous=True)
	#rospy.init_node('mavcmd', anonymous=True)

	mavros.set_namespace('/mavros')
	rospy.init_node('time', anonymous=True)
	return rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)

# Set the mode of the UAV
def set_mode(custom_mode='GUIDED', base_mode=0):
	print 'Setting mode to (%d, %s)' % (base_mode, custom_mode)
	try:
		set_mode = rospy.ServiceProxy(mavros.get_topic('set_mode'), SetMode)
		ret = set_mode(base_mode=base_mode, custom_mode=custom_mode)
	except rospy.ServiceException as ex:
		fault(ex)

	if not ret.success:
		fault('Request failed. Check mavros logs')

# Arm the UAV
def arm():
	try:
		ret = command.arming(value=True)
	except rospy.ServiceException as ex:
		fault(ex)

	if not ret.success:
		fault('Request failed. Check mavros logs')

	return ret

# Takeoff with the UAV
def takeoff(altitude=0.1):
	print 'Taking off'
	try:
		ret = command.takeoff(
			min_pitch=0,
			yaw=0,
			latitude=0,
			longitude=0,
			altitude=altitude)
	except rospy.ServiceException as ex:
		fault(ex)

	if not ret.success:
		fault('Request failed. Check mavros logs')

# Land the UAV
def land(altitude=0):
	print 'Landing'
	try:
		ret = command.land(
			min_pitch=0,
			yaw=0,
			latitude=0,
			longitude=0,
			altitude=altitude)
	except rospy.ServiceException as ex:
		fault(ex)

	if not ret.success:
		fault('Request failed. Check mavros logs')

# Move the UAV
def publish_once(pub, msg):
	_ONCE_DELAY = 3

	pub.publish(msg)

	rospy.sleep(0.2)

	try:
		command.guided_enable(value=True)
	except rospy.ServiceException as ex:
		fault(ex)

	# stick around long enough for others to grab
	timeout_t = rospy.get_time() + _ONCE_DELAY
	while not rospy.is_shutdown() and rospy.get_time() < timeout_t:
		rospy.sleep(0.2)
		print_if(pub.get_num_connections() < 1,
			 'Mavros not started, nobody subcsribes to', pub.name)

def throttle_yaw_pitch_roll(publisher,throttle=1500,yaw=0,pitch=0,roll=0):
	print 'Throttle', throttle
	print 'Yaw', yaw
	print 'pitch', pitch
	print 'roll', roll
	min_val = 1000;
	max_val = 2000;

	if len( filter( lambda x: (x < min_val or x > max_val) and x != 0, [roll, pitch, throttle, yaw] ) ) > 0:
		print 'Values must be between %d and %d' % (min_val, max_val)
		return

	msg = OverrideRCIn()
	msg.channels[0] = roll
	msg.channels[1] = pitch
	msg.channels[2] = throttle
	msg.channels[3] = yaw
	msg.channels[4] = 1100
	msg.channels[5] = 1100
	msg.channels[6] = 1100
	msg.channels[7] = 1100

	publisher.publish(msg)

def move(publisher,amount,action,duration=1):
	change = amount * 100
	throttle_yaw_pitch_roll(publisher,**{ action: (1500 + change)})
	time.sleep(duration)
	throttle_yaw_pitch_roll(publisher)

def forward(publisher,amount,duration=1):
	move(publisher,amount,'pitch',duration)

def left(publisher, amount,duration=1):
	move(publisher,amount,'roll',duration)

def up(publisher, amount,duration=1):
	move(publisher,amount,'throttle',duration)

# Application entry point
if __name__ == '__main__':
	publisher = init()
	while True:
		cs = raw_input('>').split()
		c = cs[0]
		if c == 'exit' or c == 'quit':
			break
		elif c == 'emanuel' or c == 'manual':
			param_set('SYSID_MYGCS', 255)
		elif c == 'auto':
			param_set('SYSID_MYGCS', 1)
		elif c == 'guided':
			set_mode('GUIDED')
		elif c == 'stabilize':
			set_mode('STABILIZE')
		elif c == 'hold':
			set_mode('ALT_HOLD')
		elif c == 'arm':
			arm()
		elif c == 'toffman':
			up(publisher,500,2)
		elif c == 'takeoff':
			takeoff(altitude=float(cs[1]))
		elif c == 'land':
			land()
			break
		elif c == 'forward':
			v = float(cs[1])
			forward(publisher,v)
		elif c == 'backward':
			v = float(cs[1])
			forward(publisher,-v)
		elif c == 'left':
			v = float(cs[1])
			left(publisher,v)
		elif c == 'right':
			v = float(cs[1])
			left(publisher,-v)
		elif c == 'up':
			v = float(cs[1])
			up(publisher,v)
		elif c == 'down':
			v = float(cs[1])
			up(publisher,-v)
		elif c == 'raw':
			throttle_yaw_pitch_roll(publisher, *map(int, cs[1:]))
		elif c == 'control':
			pass	
		else:
			print 'Invalid command'
