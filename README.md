<<<<<<< HEAD
# cs470
Classwork for CS470 Intro to AI
=======
This project is forked from Sphero ROS( https://github.com/mmwise/sphero_ros ).

BB-8 driver (from https://github.com/jchadwhite/SpheroBB8-python) is used in creating ROS node support.

sphero_ros
==========

checkout the [docs](http://dqyi11.github.com/sphero_ros)

=======
## Installation
Installation is now based on catkin:

      cd <ws>/src
      git clone https://github.com/dqyi11/sphero_ros
      cd <ws>
      catkin_make
      catkin_make install
      source <ws>/install/setup.bash
      ...

## BB8 driver
The connection is through BLUETOOTH LE

      hcitool dev
      hcitool (-i hci1) lescan
      hciconfig hci0 up/down

>>>>>>> 073163c36516af8b60b52f9db2c8ab4d3fdd7ef2
