# Intel&reg; Euclid&trade; Automation Nodes - Network manager node.

This network manager node is reponsible for handling device network connectivity , Wifi discovery, Hotspot publishing.

[Intel® Euclid™ Community Site](http://www.euclidcommunity.intel.com).

[Intel® Euclid™ Support Forum](http://www.intel.com/content/www/us/en/support/emerging-technologies/intel-euclid-development-kit.html).

## Subscribed Topics 
None

## Published Topics
    None    
	
## Services 
    /euclid/network/scan (network_manager/handle_scanNetworks)
        Call for wifi network scan flow.
    /euclid/network/list (network_manager/handle_getNetworksList)
        Get list of existing known WiFi networks
    /euclid/network/get_saved_networks (network_manager/handle_getSavedNetworks)
        Get list of registered WiFi networks
    /euclid/network/connect (network_manager/handle_registerNetwork)
        Call to connect to known WiFi with ssid and password.
    /euclid/network/connect_to_saved_network (network_manager/handle_connectToSavedNetwork)
        Call to connect to known SSID.
    /euclid/network/start_hotspot (network_manager/handle_startHotspot)
        Call to connect to Hotspot.        
    /euclid/network/set_ros_master_uri (network_manager/handle_setROSMasterURI)
        Update ROS Master URI to specified address.
    /euclid/network/get_current_connection_name (network_manager/handle_getCurrentConnectionName)
        Get current Connection name if connected.
    
    
## Contributing to the Project

The Intel&reg; Euclid&trade; Network manager node is developed and distributed under
a BSD-3 license as noted in [License file](LICENSE).

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
have the right to submit it under the open source license
indicated in the file; or

(b) The contribution is based upon previous work that, to the best
of my knowledge, is covered under an appropriate open source
license and I have the right under that license to submit that
work with modifications, whether created in whole or in part
by me, under the same open source license (unless I am
permitted to submit under a different license), as indicated
in the file; or

(c) The contribution was provided directly to me by some other
person who certified (a), (b) or (c) and I have not modified
it.

(d) I understand and agree that this project and the contribution
are public and that a record of the contribution (including all
personal information I submit with it, including my sign-off) is
maintained indefinitely and may be redistributed consistent with
this project or the open source license(s) involved.

## Configuration:

| Version        | Best Known           |
|:-------------- |:---------------------|
| OS             | Ubuntu 16.04 LTS     |
| ROS            | Kinetic              |
