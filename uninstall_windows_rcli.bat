@echo off
echo Uninstalling ceilomoeter client...
pip uninstall python-swiftclient
pip uninstall python-ceilometerclient
echo done
echo -----------------------

echo Uninstalling cinder client...
pip uninstall python-cinderclient
echo done
echo -----------------------

echo Uninstalling glance client...
pip uninstall python-glanceclient
echo done
echo -----------------------


echo Uninstalling heat client...
pip uninstall python-heatclient
echo done
echo -----------------------


echo Uninstalling keystoneauth...
pip uninstall keystoneauth1
echo done
echo -----------------------

echo Uninstalling keystone client...
pip uninstall python-keystoneclient
echo done
echo -----------------------

echo Uninstalling neutron client...
pip uninstall python-neutronclient
echo done
echo -----------------------

echo Uninstalling nova client...
pip uninstall python-novaclient
echo done
echo -----------------------

echo Uninstalling openstack client...
pip uninstall python-openstackclient
echo done
echo -----------------------

echo Uninstalling openstack sdk...
pip uninstall python-openstacksdk
echo done
echo -----------------------

echo Uninstalling Wind River System client...
pip uninstall httplib2 python-dateutil cgtsclient
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