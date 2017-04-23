cmake_minimum_required(VERSION 2.8.3)
project(network_manager)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)


## Generate services in the 'srv' folder
add_service_files(
  FILES
  CsDisconnectNetwork.srv
  CsGetCurrentConnectionName.srv
  CsNetworksList.srv
  CsStartHotspot.srv
  CsSetROSMasterURI.srv
  CsScanNetworks.srv
  CsGetSavedNetworks.srv
  CsConnectToSavedNetwork.srv
  CsConnectToNetwork.srv
)

# Install python scripts using distutils
catkin_python_setup()

## Generate added messages and services with any dependencies listed here
generate_messages(
 DEPENDENCIES
   std_msgs
)


catkin_package(
 CATKIN_DEPENDS roscpp rospy std_msgs
 CATKIN_DEPENDS message_runtime
)

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############

# Load catkin and all dependencies required for this package
set(CATKIN_DEPS std_msgs rospy)

# Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)



catkin_package(
    DEPENDS ${SYS_DEPS}
    CATKIN_DEPENDS ${CATKIN_DEPS}
)

catkin_install_python(PROGRAMS scripts/CsNetworkConfigModule.py
                      DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
