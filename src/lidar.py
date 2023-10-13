#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# NOTE: 이 모듈은 곧 lidar_ 에 의해 리팩터링될 모듈이므로, 나중에는 사용하지 말 것.

# 외장
import time
import math

# 서드파티
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Range       # 시각화
from sensor_msgs.msg import LaserScan   # 라이다 센서 데이터

rospy.init_node('lidar')

lidar_points = None

def lidar_callback(data):
    global lidar_points
    lidar_points = data.ranges

rospy.Subscriber('scan', LaserScan, lidar_callback, queue_size=1)
pub_front = rospy.Publisher('scan_front', Range, queue_size=1)
pub_front_right_60 = rospy.Publisher('scan_front_right_60', Range, queue_size=1)
pub_front_left_60 = rospy.Publisher('scan_front_left_60', Range, queue_size=1)
pub_back = rospy.Publisher('scan_back', Range, queue_size=1)
pub_left = rospy.Publisher('scan_left', Range, queue_size=1)
pub_right = rospy.Publisher('scan_right', Range, queue_size=1)

msg = Range()
h = Header()

fov = 60

msg.radiation_type = Range().ULTRASOUND
msg.min_range = 0.05
msg.max_range = 20.0
msg.field_of_view = (fov / 180.0) * 3.14


def get_fovidx(points, angle):
    """
    points: tuple, angle: int
    return: tuple

        [(s1, e1), (s2, e2)] 또는 [(s, e)] 를 리턴
        sn, en 은 반드시 정수
    """
    global fov
    assert angle >= 0 and angle <= 360
    assert fov < 180
    angle_per_point = 360.0 / len(points)
    s = ((360 + angle - fov // 2) % 360)
    e = ((360 + angle + fov // 2) % 360)
    s = int(math.floor(s / angle_per_point))
    e = int(math.ceil(e / angle_per_point))
    ret = []
    if s > e:
        ret.append((s, len(points)))
        ret.append((0, e))
    else:
        ret.append((s, e))
    return ret


def get_fovavg(points, angle):
    global fov
    sum_ = 0
    sum_len = 0
    for s, e in get_fovidx(points, angle):
        sum_ += sum(points[s:e])
        sum_len += (e - s)
    assert sum_ >= 0
    assert sum_len > 0
    return sum_ / sum_len


while not rospy.is_shutdown():
    if lidar_points == None:
        continue

    h.frame_id = "right"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 90)
    pub_right.publish(msg)

    h.frame_id = "front_right_60"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 300)
    pub_front_right_60.publish(msg)

    h.frame_id = "front"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 0)
    pub_front.publish(msg)

    h.frame_id = "front_left_60"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 60)
    pub_front_left_60.publish(msg)

    h.frame_id = "left"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 270)
    pub_left.publish(msg)

    """h.frame_id = "back"
    msg.header = h
    msg.header.stamp = rospy.Time.now()
    msg.range = get_fovavg(lidar_points, 180)
    pub_back.publish(msg)"""

    time.sleep(0.1)
