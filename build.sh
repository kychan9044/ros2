#!/bin/sh

colcon build --symlink-install
source install/local_setup.bash 

if [${1} -eq "0"];then
    ros2 run cat camera_publisher
fi 

if [${1} -eq "1"];then
    ros2 run cat camera_subscriber
fi 
