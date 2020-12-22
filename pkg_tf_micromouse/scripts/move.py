#!/usr/bin/env python
from geometry_msgs.msg import Twist
import rospy
import math
import time

def GoToNextCell() :
    x_vel=0.1
    
    msg=Twist()
    msg.linear.x=x_vel
    msg.linear.y=0
    msg.linear.z=0
    msg.angular.x=0
    msg.angular.y=0
    msg.angular.z=0

    pub=rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move', anonymous=True)

    rate=rospy.Rate(10)

    
    for x in range (72*4) :
        pub.publish(msg)
        time.sleep(0.1)

    msg.linear.x=0
    msg.angular.z=0

    for x in range (40) :
        pub.publish(msg)
        rate.sleep()

def left() :
    z_vel=1.578/2
    
    msg=Twist()
    msg.linear.x=0
    msg.linear.y=0
    msg.linear.z=0
    msg.angular.x=0
    msg.angular.y=0
    msg.angular.z=z_vel

    pub=rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move', anonymous=True)

    rate=rospy.Rate(10)

    for x in range (25) :
        pub.publish(msg)
        rate.sleep()

    msg.angular.z=0

    for x in range (40) :
        pub.publish(msg)
        rate.sleep()

    
    
if __name__ == '__main__' :
    try:
        GoToNextCell()
    except rospy.ROSInterruptException:
        pass	


