import rospy
from geometry_msgs.msg import Pose2D

import numpy as np

topic = "GPS"
'''
X = []
Y = []
'''
def write_to_file(msg):
    '''global X, Y
    X.append(msg.x)
    Y.append(msg.y)'''
    coordinates = open("map_plot.txt", mode = "a+")
    coordinates.write("{x}, {y}\n".format(x = msg.x, y = msg.y))# msg.x,msg.y)
    coordinates.close()

def listener():
    rospy.init_node("plotter",anonymous= True)
    sub = rospy.Subscriber(topic, Pose2D, callback= write_to_file)
    rospy.spin()

listener()