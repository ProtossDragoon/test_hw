#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 외장
import math

# 서드파티
import rospy
from sensor_msgs.msg import Range


class LidarHelper():

    def __init__(
        self,
        fov: int
    ):
        self.fov = fov # FIXME
        self.msg_range = Range()
        self.msg_range.field_of_view = (fov / 180.0) * 3.14

    def get_msg_range(
        self,
        fov: int = None,
        new_object: bool = False
    ) -> Range:
        msg = self.msg_range
        if new_object:
            msg = Range()
        msg.header.stamp = rospy.Time.now()

    def get_fovidx(
        self,
        points: tuple,
        angle: int,
    ) -> list:
        """
        Returns:
            [(s1, e1), (s2, e2)] 또는 [(s, e)] 를 리턴
            sn, en 은 반드시 정수
        """
        assert angle >= 0 and angle <= 360
        assert self.fov < 180
        angle_per_point = 360.0 / len(points)
        s = ((360 + angle - self.fov // 2) % 360)
        e = ((360 + angle + self.fov // 2) % 360)
        s = int(math.floor(s / angle_per_point))
        e = int(math.ceil(e / angle_per_point))
        ret = []
        if s > e:
            ret.append((s, len(points)))
            ret.append((0, e))
        else:
            ret.append((s, e))
        return ret


    def get_fovavg(
        self,
        points: tuple,
        angle: int,
    ):
        sum_ = 0
        sum_len = 0
        for s, e in self.get_fovidx(points, angle):
            sum_ += sum(points[s:e])
            sum_len += (e - s)
        assert sum_ >= 0
        assert sum_len > 0
        return sum_ / sum_len
