#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from xycar_msgs.msg import xycar_motor    # 모터 제어를 위한 토픽 메시지 타입

motor_control = xycar_motor()

rospy.init_node('motor_test')    # 'auto_driver' 이름으로 노드 초기화

pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1) # xycar_motor 토픽의 발행 준비

def motor_pub(angle, speed): # angle, speed 값을 인자로 받아 xycar_motor 토픽으로 발행
	global pub
	global motor_control

	motor_control.angle = angle
	motor_control.speed = speed
	
	pub.publish(motor_control)

speed = 3    # 구동 속도를 3으로 설정 (천천히 주행)
while not rospy.is_shutdown():
	# angle = -50    # 좌회전 최대
	# for i in range(40):
	# 	motor_pub(angle, speed)
	# 	time.sleep(0.1)

	angle = 0    # 직진
	for i in range(30):
		motor_pub(angle, speed)
		time.sleep(0.1)

	# angle = 50    # 우회전 최대
	# for i in range(40):
	# 	motor_pub(angle, speed)
	# 	time.sleep(0.1)

	angle = 0    # 정지
	for i in range(30):
		motor_pub(angle, 0)
		time.sleep(0.1)
