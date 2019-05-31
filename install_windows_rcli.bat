@echo off
echo This batch file installs the Titanium Remote Clients version b14.
echo Note: this batch file does no error checking, and blindly tries to install
echo requirements (whether requirements.txt exists or not) so be careful.
:: Author: Rich Moore, rmoorewrs@gmail.com

:: We should be starting in the main directory of the git repo
cd wrs-remote-clients-2.0.2
echo Installing requirements ...
pip -q install -r requirements.txt -c upper_constraints.txt
echo done
echo -----------------------
 
:: now go into each subdirectory and do install for that package

:: ceilometer
echo Installing ceilomoeter client...
cd python-ceilometerclient-2.9.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: cinder
echo Installing cinder client...
cd python-cinderclient-3.1.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: glance
echo Installing glance client...
cd python-glanceclient-2.8.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: heat
echo Installing heat client...
cd python-heatclient-1.11.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
echo done
echo -----------------------

:: keystone Auth
echo Installing keystoneauth...
cd python-keystoneauth1-3.1.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: keystone client
echo Installing keystone client...
cd python-keystoneclient-3.13.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: neutron
echo Installing neutron client...
cd python-neutronclient-6.5.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: nova
echo Installing nova client...
cd python-novaclient-9.1.1
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: openstack client
echo Installing openstack client...
cd python-openstackclient-3.12.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: openstack sdk
echo Installing openstack sdk...
cd python-openstacksdk-0.9.17
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: wrs system
echo Installing Wind River System client...
cd python-wrs-system-client-1.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

:: osclib
echo Installing osc-lib-1.7.0
cd osc-lib-1.7.0
pip -q install -r requirements.txt -c ..\upper_constraints.txt
python setup.py -q install
cd ..
echo done
echo -----------------------

echo Installing dependency for the openrc2bat.py utility...
pip -q install docopt
echo done
echo -----------------------

echo:
echo ----------------------- 
echo Note:
echo ----------------------- 
echo You must convert an OpenStack credentials file to a batch file and run this each time before 
echo using the remote clients.
echo:   
echo Step 1) Download your credentials file from Horizon (Project->Compute->AcccessSecurity->Download OpenStack RC File v3)
echo Step 2) Convert the file (e.g. admin-openrc.sh) to a batch file with the openrc2bat.py utility.
echo:   
echo        python openrc2bat.py --pass my-password admin-openrc.sh my-openrc.bat
echo:     
echo Step 3) After opening a new CMD shell in Windows, run your credentials batch file 
echo         (e.g. 'my-openrc.bat') before using the remote clients