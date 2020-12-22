#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np
#import math

pi=3.14159265
x_dist = 0
y_dist= 0
lis = []


def clbk_odom(msg):
    global x_dist
    global y_dist
    global yaw
    

    # position
    position_ = msg.pose.pose.position
    # gives x and y distance of the bot
    x_dist = position_.x
    y_dist = position_.y




    
    # yaw
    # convert quaternions to euler angles, only extracting yaw angle for the robot
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    
    yaw = euler[2]
    #print(x_dist, y_dist)
    lis.append(yaw)





#def clbk_laser(msg):
    #'p' : msg.ranges[:],
    ###print region['p'][i]

def main():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom) 
    #sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)  
    rospy.init_node('cmd_robot', anonymous=True)
    rate = rospy.Rate(100) # 40hz
    initial =lis[0]
    print(initial)
   
    msg1 = Twist()

    while not rospy.is_shutdown():
        current= lis[-1]
        
        
        
        if (abs(current-initial)<pi/2):
            msg1.linear.x = 0
    
            msg1.angular.z = 0.7
            pub.publish(msg1)
            rate.sleep()
        else :
            msg1.angular.z =0
            pub.publish(msg1)
            rate.sleep()

        

        # for i in range(500):

            
            
	    # #positive speed_z value represents clockwise angular velocity of the bot and positive speed_x value represents forward linear velocity of the robot

        #     msg1.linear.x = 0.1
    
        #     msg1.angular.z = 0
        #     pub.publish(msg1)
        #     rate.sleep()
        # while not rospy.is_shutdown():
        #     msg1.linear.x =0
        #     pub.publish(msg1)


if __name__ == '__main__':
    main()
