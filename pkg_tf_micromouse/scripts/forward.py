#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
import numpy as np


x_dist = 0
y_dist= 0
lis = []
front=1
left=1
right=1



def clbk_odom(msg):
    global x_dist
    global y_dist
    global yaw_
    
    

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
    
    yaw_ = euler[2]
    #print(x_dist, y_dist)
    lis.append([x_dist,y_dist])

def dist(a,b):
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)



def clbk_laser(msg):
    global front
    global left
    global right

    right = min(min(msg.ranges[0:30]), 10)
    #'fright': min(min(msg.ranges[72:143]), 10),
    front = min(min(msg.ranges[175:185]), 10)
        #'fleft':  min(min(msg.ranges[216:287]), 10),
    left = min(min(msg.ranges[329:359]), 10)
    print (front,left,right)
   

    

    
        

def main():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom) 
    sub = rospy.Subscriber('/my_mm_robot/laser/scan', LaserScan, clbk_laser)  
    rospy.init_node('cmd_robot', anonymous=True)
    rate = rospy.Rate(20) # 40hz
    initial =lis[0]
    print(initial)
   
    msg1 = Twist()

    while not rospy.is_shutdown():
        current= lis[-1]
        
        
        # if front < 0.3 :
        #     msg1.linear.x = 0
        #     msg1.angular.z = 0
        #     pub.publish(msg1)
        #     print('case1')           
        #     rate.sleep()
        if (dist(initial,current)<0.18):
            if front < 0.08 :
                msg1.linear.x = 0
                msg1.angular.z = 0
                pub.publish(msg1)
                print('case4')
                exit()
            
            if right < 0.06 :
                msg1.linear.x = 0.4
                msg1.angular.z = 0.02
                print('case1')
            elif left < 0.06 :
                msg1.linear.x = 0.4
                msg1.angular.z = -0.02
                print('case2')
            else:
            
                msg1.linear.x = 0.4
                msg1.angular.z = 0
                print('case3')
            
            pub.publish(msg1)
            rate.sleep()
        else :
            msg1.linear.x =0
            msg1.angular.z =0
            pub.publish(msg1)
            rate.sleep()
	    exit()
    

        

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
