#!/usr/bin/env python

##################################################################################
#Copyright (c) 2016, Intel Corporation
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation
#and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors
#may be used to endorse or promote products derived from this software without
#specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##################################################################################

import os
import time
import rospy
from std_msgs.msg import String
from network_manager.srv import *
from NetworkFlowFacade import NetworkFlowFacade

class CsNetworkManager(object):
    def __init__(self):
        rospy.logdebug('Init CsNetworkManager')
        
    def handle_scanNetworks(self, req):
        '''
        * Call for rescan of networks.
        * System post async message request which: do:
            if currently connected to Hotspot:
                *** Stop IP Discovery sender
                *** Disconnect Hotspot.
                *** Run Rescan networks
                *** Save in available networks list.
                *** Reconnect to hotspot        
            Else:
                *** Run Rescan networks
                *** Save in available networks list.
        :return: True if message posted, otherwise False. --  CsScanNetworksResponse(True / False).
        '''
        try:
            rospy.logdebug('Call Network Scan')
            requestPosted = NetworkFlowFacade.RequestNetworkRescan()
            
            return CsScanNetworksResponse(requestPosted)
        except Exception as e:
            rospy.logerr('Scan Networks Failed, Error: {}'.format(str(e.message)))
            return CsScanNetworksResponse(False)           
      
    def handle_getNetworksList(self, req):
        '''
        Get list of existing WiFi networks
        :return: CsNetworksListResponse(lastUpdateTime, wifiList).  
        '''
        try:
            wifiList = NetworkFlowFacade.GetAvailableNetworkList()
            lastUpdateTime = None # FIXME
            return CsNetworksListResponse(str(lastUpdateTime),wifiList)
        except Exception as e:
            rospy.logerr('Get Network List Failed, Error: {}'.format(str(e.message)))
            return 'Get Network List Failed, Error: {}'.format(str(e.message))
    
    def handle_getSavedNetworks(self, req):
        '''
        Get list of registered WiFi networks
        Return: CsGetSavedNetworksResponse(wifiList).  
        '''
        try:
            wifiList = NetworkFlowFacade.GetRegisteredNetworks()
            return CsGetSavedNetworksResponse(wifiList)
        except Exception as e:
            rospy.logerr('Get Saved Networks Failed, Error: {}'.format(str(e.message)))
    
    def handle_registerNetwork(self, req):
        '''
        Call to connect to known WiFi with ssid and password.
        request have ssid and password.
        * System post async message request which: do:
            Verify requested SSID is in the known wifi list and abort if it is not.
            * Hold current connection name.
            * Stop current ip address publishing.
            * Call to register and connect to new network.
            *** If Connectd:
                ** Update SSID name in config (effective for next restart.)
                ** Reconnect previous SSID.
                ** Restart IP Discovery sender.
                ** Response with message that restart is required. 
            *** Else
                ** Return Error message
            :return: tuple of True/ False if operation done, Message to describe process.
        '''
        try:            
            rospy.logdebug('Call Network Scan')
            ssid = req.ssid
            password = req.password

            if(ssid is None or ssid == ''):
                return CsConnectToNetworkResponse(False, 'SSID is Null.')   
                
            if(password is None):
                return CsConnectToNetworkResponse(False, 'password is Null.')   
      
            requestPosted = NetworkFlowFacade.RequestRegisterNetwork(ssid, password)

            return CsConnectToNetworkResponse(requestPosted, 'Please connct to wifi: {0}'.format(ssid))
        except Exception as e:
            rospy.logerr('Register Network Failed, Error: {}'.format(str(e.message)))
            return CsConnectToNetworkResponse(False, str(e.message))

    def handle_connectToSavedNetwork(self, req):
        '''
        Call to connect to known SSID.
        * System post async message request which: do:
            Verify requested ssid is in registered network list.
            Update SSID name in config (effective for next restart.)
        :return: True if message posted, otherwise False.
        '''
        try: 
            ssid = req.ssid

            if(ssid is None or ssid == ''):
                return CsConnectToNetworkResponse(False, 'SSID is Null.')

            requestPosted = NetworkFlowFacade.RequestConnectNetwork(ssid)
            return CsConnectToSavedNetworkResponse (requestPosted, 'Operation Done. Please connct to wifi: {0}'.format(ssid))
        except Exception as e:
            rospy.logerr('Connect To Saved Network Failed, Error: {}'.format(str(e.message)))
            return CsConnectToSavedNetworkResponse (False, str(e.message))

    def handle_setROSMasterURI(self, req):
        '''
        Update ROS Master URI to specified address.
        Request have updated URI.
        Return: True if operation done, Otherwise false.
        '''
        try:
            self._updateRosMasterURI(req.ros_master_uri)
            return CsSetROSMasterURIResponse(True)
        except Exception as e:
            rospy.logerr('Set ROS Master URI Failed, Error: {}'.format(str(e.message)))

    def handle_getCurrentConnectionName(self,req):
        '''
        get current Connection name if connected
        :return: Connection name or empty if not connected, and or error if exists.
        '''
        try:
            connectionName = NetworkFlowFacade.GetCurrentConneectionName()
            return CsGetCurrentConnectionNameResponse(connectionName)
        except Exception as e:
            rospy.logerr('Get Current Connection Name Failed, Error: {}'.format(str(e.message)))

    def handle_startHotspot(self, req):
        '''
        Call to connect to Hotspot.
        Update SSID name in config (effective for next restart.)
        :return: true
        '''
        try:
            requestPosted = NetworkFlowFacade.RequestConnectHotspot()            
            return CsStartHotspotResponse(requestPosted)
        except Exception as e:
            rospy.logerr('Start Hotspot Failed, Error: {}'.format(str(e.message)))

    def _updateSSID(self, value):
        '''
        Call to update settings file with requested ssid.
        Update SSID name in config (effective for next restart.)
        '''
        self._updateSettingsFile('ssid',value)
            
    def _updateRosMasterURI(self, ipAddress):
        
        updatedRosURI = ipAddress 
        
        # call update settings file
        self._updateSettingsFile('ROSMasterURI',updatedRosURI)

        updatedRosURI = updatedRosURI.replace('{IP_ADDR}', ipAddress)

        cmd = 'bash -c \'echo "export ROS_MASTER_URI={IP_ADDRESS}" >> ~/.bashrc\''
        cmd = cmd.replace('{IP_ADDRESS}', updatedRosURI)
        os.system(cmd)
        os.system('bash -c \'source ~/.bashrc\'')

    def _updateSettingsFile(self, key, value):
        replacement=key + "=" + value
        cmd = "sed -i '/" + key + "/c\'" + replacement +  " /intel/euclid/config/settings.ini"
        os.system(cmd)     

    def StartRosService(self):
        rospy.init_node('CsNetworkManager')
       
        rospy.Service('/euclid/network/scan',CsScanNetworks,self.handle_scanNetworks)
        rospy.Service('/euclid/network/list', CsNetworksList, self.handle_getNetworksList)
        rospy.Service('/euclid/network/get_saved_networks',CsGetSavedNetworks,self.handle_getSavedNetworks)        
        rospy.Service('/euclid/network/connect',CsConnectToNetwork,self.handle_registerNetwork)
        rospy.Service('/euclid/network/connect_to_saved_network',CsConnectToSavedNetwork,self.handle_connectToSavedNetwork)
        rospy.Service('/euclid/network/start_hotspot',CsStartHotspot,self.handle_startHotspot)
        rospy.Service('/euclid/network/set_ros_master_uri',CsSetROSMasterURI,self.handle_setROSMasterURI)
        rospy.Service('/euclid/network/get_current_connection_name',CsGetCurrentConnectionName,self.handle_getCurrentConnectionName)

        print "Ready to manage wifi."
        rospy.spin()


if __name__ == '__main__':
    try:
        manager = CsNetworkManager()
        manager.StartRosService()
    except rospy.ROSInterruptException as rosE:
        rospy.logerr(str(rosE))        
        pass
    except Exception as e:
        rospy.logerr(str(e))        
        pass
