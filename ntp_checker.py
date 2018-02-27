#!/usr/bin/python

#################################################################################
#
# Author : Lukesh Meshram - for UBS
# Date   : 27/02/2018
# Purpose: To verify NTP is syncing correctly on RHEL 6/7 and Solaris 10 server.
# Tested : Linux RHEL 6/7 and Solaris 10
# Python : Works fine on Python 2.6 and above
#
#################################################################################

import platform
import sys
import os
from subprocess import *
import datetime

def display_date():
        now = datetime.datetime.now()
        timee = now.strftime("%Y-%m-%d %H:%M")
        info = '[ INFO     ]: ' + timee
        warn = '[ WARN\'g  ]: ' + timee
        crit = '[ CRITICAL ]: ' + timee


# Function to check if current distrubution and Release version is-line to estate (RHEL 6/7 & Solaris 10)
def platform_check():
        if platform.system() == 'Linux':
                if (platform.dist()[0] == 'redhat'):
                        rhel = open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0]
                        if (rhel == '7' or rhel == '6'):
                                action = 'go'
                        else:
                                print "Unsupport RHEL version:" + rhel + ",exiting"
                                sys.exit(1)
                else:
                        print "Unsupport Linux distrubution:" + platform.dist()[0] + " ,exiting"
                        sys.exit(1)
        else:
                if platform.system() == 'SunOS':
                        if platform.release().split('.')[1] == '10':
                                action = 'go'
                        else:
                                print "Unspport SunOS version: " + platform.release().split('.')[1] + ", exiting"
                                sys.exit(1)
                else:
                        print "Unsupport Unix platfrom: " + platform.system() + " ,exiting"
                        sys.exit(1)

# Function to collect and compair the NTP offset values
def ntp_status_check():

        DEVNULL = open('/dev/null', 'w')
        # Setting warning and critical threshold values
        warning_value = 50
        critical_value = 100

        # ntpq command Path value
        CMD_ntpq = '/usr/sbin/ntpq'
        # checking if the ntpq command exists
        if not os.path.isfile(CMD_ntpq):
                print "NTP client binary not install, exiting"
                sys.exit(1)

        # Collecting offset value for the selected NTP server '*'
        cmd = '/usr/sbin/ntpq -pn | egrep \'^\*\' | awk \'{ print $9 }\' | tr -d \'-\''
        output = Popen(cmd, shell=True, stdout=PIPE, stderr=DEVNULL)
        offset_value_selected_source = output.communicate()[0].rstrip()
        # if offset value if empty, exiting as needs to further investigate
        if not offset_value_selected_source:
                print "Collection of NTP offset was unsucessfull, please check if the ntp is operating normally"
                sys.exit(1)
        if float(offset_value_selected_source) > critical_value:
                print "NTP offset reached its CRITICAL threshold, check ASAP!!"
        elif float(offset_value_selected_source) > warning_value:
                print "NTP offset crossed it WARNING threshold, you can take your time to check"
        else:
                print "NTP offset is under CONTROL"


if __name__ == "__main__":
        platform_check()
        ntp_status_check()
