#!/bin/sh

git pull
colcon build --symlink-install
source install/local_setup.bash 
