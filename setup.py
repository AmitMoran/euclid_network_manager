from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup


setup(
	name='network_manager',
    version='1.0.0',
    scripts=['scripts/CsNetworkConfigModule.py'],
    packages=['network_manager'],
    package_dir={'': '/intel/euclid/euclid_ws/src/system_nodes/'}
)


