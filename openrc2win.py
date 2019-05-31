#!/usr/bin/env python

# do not change this block, it is used by docopt to parse the command line parameters
"""Usage:  openrc2win [-hv] [--pass <pwd>] [--cert <pem_file>] <rc_file> <windows_output_name>

Options:
  -h --help                 Print this information
  -v                        Verbose
  -p <pwd> --pass <pwd>     OpenStack password for host/project/user you're connecting to
  -c <pwd> --cert <pwd>     CA cert pem file for HTTPS authentication

"""

import sys
import os
from docopt import docopt

def get_creds_from_env():
    creds = {}
    creds['username'] = os.environ['OS_USERNAME']
    creds['password'] = os.environ['OS_PASSWORD']
    creds['auth_url'] = os.environ['OS_AUTH_URL']
    creds['project_name'] = os.environ['OS_PROJECT_NAME']
    creds['username'] = os.environ['OS_USERNAME']
    creds['api_key'] = os.environ['OS_PASSWORD']
    creds['auth_url'] = os.environ['OS_AUTH_URL']
    creds['project_id'] = os.environ['OS_PROJECT_NAME']
    return creds

# extract the credentials from a standard openstack rc script
def get_creds_from_file(filename, password=None, cacert=None):
    creds = {}
    with open(filename, 'r') as file:
        for line in file:
            if len(line) > 1:
                line = line.replace('"','') # strip out quotes
                words = line.split() # split on whitespace

                if words[0] == 'export':
                    line = words[1]
                    words = line.split('=')
                    # handle password
                    if words[0] == 'OS_PASSWORD':
                        if password is None:
                            words[1] = raw_input("Please enter your OpenStack Password for project " + creds['OS_PROJECT_NAME'] + " as " + creds['OS_USERNAME'] + " ")
                        else:
                            words[1]=password

                    # handle CA certificate file
                    if words[0] == 'OS_CACERT':
                        if cacert is None:
                            words[1] = raw_input(
                                'Please enter a path for your CA certificate pem file, or press enter if you are not using HTTPS ')
                        else:
                            words[1]=cacert
                    # go ahead and set the value of the dict key
                    creds[words[0]] = words[1]
    return creds

# Create a DOS batch file with OS credentials for Winddows users
def save_creds_as_dos_batch(filename, creds):
    outfilename = filename + '.bat'
    with open(outfilename,'w') as file:
        for key,val in creds.items():
            # print('set ' + key + '=' + val + '\n')
            file.write('set ' + key + '=' + str(val) + '\n')
    print 'Wrote credentials to ' + outfilename

# Create a windows powershell script with OS credentials for Winddows users
def save_creds_as_ps1_script(filename, creds):
    outfilename = filename + '.ps1'
    with open(outfilename,'w') as file:
        for key,val in creds.items():
            # print('set ' + key + '=' + val + '\n')
            file.write('set-item env:' + key + str(val) + '\n')
    print 'Wrote credentials to ' + outfilename

def main():
    # parse command line arguments wtih docopt
    arguments = docopt(__doc__, version='openrc2bat 0.1')

    # check if password and CA cert are given as argument
    os_pass=arguments['--pass']
    if arguments['--cert'] is None:
        cert=''
    else:
        cert=arguments['--cert']

    creds = get_creds_from_file(arguments['<rc_file>'],password=os_pass,cacert=cert)
    save_creds_as_dos_batch(arguments['<windows_output_name>'],creds)
    save_creds_as_ps1_script(arguments['<windows_output_name>'],creds)
    print creds

if __name__== "__main__":
  main()
