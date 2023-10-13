#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 외장
import time

# 서드파티
import rospy
from sensor_msgs.msg import Range
from sensor_msgs.msg import LaserScan

# 프로젝트
# https://roboticsbackend.com/ros-import-python-module-from-another-package/ 참고
from lidar_helper import LidarHelper
from range_helper import RangeHelper


rospy.init_node('lidar')

lidar_points = None

def lidar_callback(data):
    global lidar_points
    lidar_points = data.ranges


# Publisher
rospy.Subscriber('scan', LaserScan, lidar_callback, queue_size=1)

# Subscribers
pub_front = rospy.Publisher(
    'distance_front',
    Range, queue_size=1)
pub_front_left_60 = rospy.Publisher(
    'distance_front_left_60',
    Range, queue_size=1)
pub_right = rospy.Publisher(
    'distance_right',
    Range, queue_size=1)
pub_front_right_60 = rospy.Publisher(
    'distance_front_right_60',
    Range, queue_size=1)
pub_left = rospy.Publisher(
    'distance_left',
    Range, queue_size=1)

_fov = 30
lidar_helper = LidarHelper(_fov) # FIXME
range_helper = RangeHelper()
range_helper.set_range(
    'front', _fov,
    frame_id='front')
range_helper.set_range(
    'front_left_60', _fov,
    frame_id='front_left_60')
range_helper.set_range(
    'right', _fov,
    frame_id='right')
range_helper.set_range(
    'front_right_60', _fov,
    frame_id='front_right_60')
range_helper.set_range(
    'left', _fov,
    frame_id='left')

FRONT = 0
FRONT_LEFT_60 = 60
RIGHT = 90
BACK = 180
FRONT_RIGHT_60 = 300
LEFT = 270

while not rospy.is_shutdown():
    if lidar_points == None:
        continue

    msg = range_helper.get_msg('front')
    msg.range = lidar_helper.get_fovavg(lidar_points, FRONT)
    pub_front.publish(msg)

    msg = range_helper.get_msg('front_left_60')
    msg.range = lidar_helper.get_fovavg(lidar_points, FRONT_LEFT_60)
    pub_front_left_60.publish(msg)

    msg = range_helper.get_msg('front_right_60')
    msg.range = lidar_helper.get_fovavg(lidar_points, FRONT_RIGHT_60)
    pub_front_right_60.publish(msg)

    msg = range_helper.get_msg('right')
    msg.range = lidar_helper.get_fovavg(lidar_points, RIGHT)
    pub_right.publish(msg)

    msg = range_helper.get_msg('left')
    msg.range = lidar_helper.get_fovavg(lidar_points, LEFT)
    pub_left.publish(msg)
