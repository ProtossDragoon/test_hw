#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 외장
import rospy, time

# 서드파티
from sensor_msgs.msg import Range

# FIXME: 이 ROS 패키지의 msg 디렉토리에 저장하지 않고 전역에 있는 xycar_motor 메시지를 가져올 것
from test_hw.msg import xycar_motor

# 메시지 객체
motor_msg = xycar_motor()
flag_turn_left = None

ultra_msg = None
distances = { # 거리 정보를 담을 딕셔너리
    'distance_front': None,
    'distance_front_left_60': None,
    'distance_front_right_60': None,
} # FIXME: callback 들이 single CPU 에서 돌아감.

def callback_f(data):
    global distances
    distances['distance_front'] = data.range

def callback_fl(data):
    global distances
    distances['distance_front_left_60'] = data.range

def callback_fr(data):
    global distances
    distances['distance_front_right_60'] = data.range

def callback_ultra(data):
    global ultra_msg
    ultra_msg = data.data

def drive_go(speed=5, angle=0):
    global motor_msg
    motor_msg.speed = speed
    motor_msg.angle = angle
    pub.publish(motor_msg)
    if (speed < 0): time.sleep(0.5)

def drive_stop():
    global motor_msg
    motor_msg.speed = 0
    motor_msg.angle = 0
    pub.publish(motor_msg)

rospy.init_node('lidar_driver')
rospy.Subscriber('scan_front', Range, callback_f, queue_size=1)
rospy.Subscriber('scan_front_left_60', Range, callback_fl, queue_size=1)
rospy.Subscriber('scan_front_right_60', Range, callback_fr, queue_size=1)
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)

time.sleep(3) # 라이다 연결을 위한 대기

while not rospy.is_shutdown():
    조건_전방_가까움 = distances['distance_front'] <= 0.6
    조건_좌측으로가는것선호 = distances['distance_front_left_60'] > distances['distance_front_right_60']
    조건_우측으로가는것선호 = not 조건_좌측으로가는것선호
    조건_전방우측_가까움 = distances['distance_front_right_60'] <= 0.4
    조건_전방좌측_가까움 = distances['distance_front_left_60'] <=0.4
    조건_전방좌측_너무너무가까움 = distances['distance_front_left_60'] <= 0.2
    조건_전방우측_너무너무가까움 = distances['distance_front_right_60'] <= 0.2

    if 조건_전방_가까움:
        if 조건_전방좌측_너무너무가까움:
            print(f'좌측 너무 가까움!')
            drive_go(speed=0, angle=-50)
            time.sleep(0.5)
            drive_go(speed=-5, angle=-50)
            time.sleep(0.5)
        elif 조건_좌측으로가는것선호:
            drive_go(angle=-50)
        else:
            print('차라리 우측으로 가자.')
        if 조건_전방우측_너무너무가까움:
            print(f'우측 너무 가까움!')
            drive_go(speed=0, angle=50)
            time.sleep(0.5)
            drive_go(speed=-5, angle=50)
            time.sleep(0.5)
        elif 조건_우측으로가는것선호:
            drive_go(angle=50)
        else:
            print('차라리 좌측으로 가자.')
    else:
        drive_go()

    time.sleep(0.1)
