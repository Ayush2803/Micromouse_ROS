#!/usr/bin/env python

import numpy as np
import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32

#ROS libraries
#ranges

def publisher(output):
    pub=rospy.Publisher('/values', Int32, queue_size=10)
    rospy.init_node('laser_read', anonymous=True)
    rate=rospy.Rate(10)
    pub.publish(output)
    rate.sleep()

def calculate(data) :

    output=0
    front=0
    left=0
    right=0
    
    scan=data.data

    ranges=scan.ranges
    l=len(ranges)
    angles=l/4
    avg1=0.0

    for i in range(angles) :
        avg=avg+ranges[i]

    avg1=avg1/angles

    avg2=0.0

    for i in range(angles, 3*angles) :
        avg2=avg2+ranges[i]

    avg2=avg2/angles

    avg3=0.0

    for i in range(3*angles, 4*angles) :
        avg3=avg3+ranges[i]

    avg3=avg3/angles

    thresh=0.1

    if (avg1> thresh):
        left=1

    if (avg2> thresh):
        front=1

    if (avg3> thresh):
        right=1

    output=left
    output*10
    output+front
    output*10
    output+right
    publisher(output)

    for x in output :
        print x
        print " "

    publisher(output)
    rospy.loginfo(output)


def subscriber():
    rospy.init_node('laser_read', anonymous=True)
    rospy.Subscriber('/my_mm_robot/laser/scan', sensor_msgs/LaserScan, calculate)
    rospy.spin()

if __name__ == '__main__' :
	try:
		subscriber()
	except rospy.ROSInterruptException:
		pass	
	


    
