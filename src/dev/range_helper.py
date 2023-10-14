#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 서드파티
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Range


class RangeHelper():

    def __init__(
        self
    ):
        self.ranges = {}

    def set_range(
        self,
        name: str,
        fov_angle: int,
        frame_id: str,
        min_range_meter:float = 0.05,
        max_range_meter:float = 20.0
    ) -> None:
        assert type(fov_angle) is int
        assert fov_angle > 0 and fov_angle <= 360
        self.ranges[name] = Range(
            header=Header(frame_id=frame_id),
            radiation_type=Range().ULTRASOUND,
            min_range=min_range_meter,
            max_range=max_range_meter,
            field_of_view=(fov_angle/180.0)*3.14
        )

    def get_msg(
        self,
        name: str
    ) -> Range:
        v = self.ranges.get(name)
        v.header.stamp = rospy.Time.now()
        return v


if __name__ == '__main__':
    range_helper = RangeHelper()
    range_helper.set_range(
        'hello_range_front',
        fov_angle=30,
        frame_id='front'
    )
    range_helper.set_range(
        'hello_range_back',
        fov_angle=60,
        frame_id='back'
    )
    rospy.init_node('hello_range_node')
    r = rospy.Rate(1)
    pub_front = rospy.Publisher('hello_range_front_pub', Range, queue_size=1)
    pub_back = rospy.Publisher('hello_range_back_pub', Range, queue_size=1)
    while not rospy.is_shutdown():
        pub_front.publish(
            range_helper.get_msg('hello_range_front')
        )
        pub_back.publish(
            range_helper.get_msg('hello_range_back')
        )
        r.sleep()
