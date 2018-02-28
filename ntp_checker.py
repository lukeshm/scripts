#!/usr/bin/python

#######################################################################################
#
# Author : Lukesh Meshram - for UBS
# Date   : 27/02/2018
# Purpose: To verify NTP is syncing correctly on RHEL 6/7 and Solaris 10 server.
# Tested : Linux RHEL 6/7 and Solaris 10
# Python : Works fine on Python 2.6 and above
#
# Logic behind result/output: This script gather the offset of connected NTP source
#                             only. It compairs the offset with preset "warning" and
#                             "critical" values, which can be change as per requirement.
#
# [root@localhost ubs]# ntpq -pn
#      remote           refid      st t when poll reach   delay   offset  jitter
# ==============================================================================
# +139.59.43.68    193.6.176.19     3 u   32  512  377   32.452    3.293 2354847
# *172.104.55.191  179.43.76.147    2 u  120  512  277   68.508    2.281 2354847 <---< offset
# +211.233.40.78   204.123.2.5      2 u   56  512  377  152.333   -6.794 2354847
#
#########################################################################################

import platform
import sys
import os
from subprocess import *
import datetime

now = datetime.datetime.now()
timee = now.strftime("%Y-%m-%d %H:%M")
green  = '\033[32m'
yellow = '\033[93m'
red    = '\033[31m'
normal = '\033[0m'
info = timee + normal + green + ' [ INFO ]: ' + normal
warn = timee + normal + yellow + ' [ WARN\'g ]: ' + normal
crit = timee + normal + red + ' [ ERROR ]: ' + normal
os.system('clear')
warning_value = 50
critical_value = 100
# Printing header
print "\n>=====Warning 50ms======> NTP Offset Checker - UBS <======Critical 100ms====<\n"

# Function to check if current distrubution and Release version is-line to estate (RHEL 6/7 & Solaris 10)
def platform_check():
        if platform.system() == 'Linux':
                if (platform.dist()[0] == 'redhat'):
                        rhel = open('/etc/redhat-release','r').read().split(' ')[6].split('.')[0]
                        if (rhel == '7' or rhel == '6'):
                                action = 'go'
                        else:
                                print crit + "Unsupport RHEL version: " + red + rhel + normal + ",exiting!\n"
                                sys.exit(1)
                else:
                        print crit + "Unsupport Linux distrubution: " + red + platform.dist()[0] + normal + " ,exiting!\n"
                        sys.exit(1)
        else:
                if platform.system() == 'SunOS':
                        if platform.release().split('.')[1] == '10':
                                action = 'go'
                        else:
                                print crit + "Unspport SunOS version: " + platform.release().split('.')[1] + ", exiting\n"
                                sys.exit(1)
                else:
                        print crit + "Unsupport Unix platfrom: " + red + platform.system() + normal + " ,exiting\n"
                        sys.exit(1)

# Function to collect and compair the NTP offset values
def ntp_status_check():
        DEVNULL = open('/dev/null', 'w')
        # ntpq command Path value
        CMD_ntpq = '/usr/sbin/ntpq'
        # checking if the ntpq command exists
        if not os.path.isfile(CMD_ntpq):
                print crit + "NTP client binary /usr/sbin/ntpq is missing , exiting\n"
                sys.exit(1)

        # Collecting offset value for the selected NTP server '*'
        cmd = '/usr/sbin/ntpq -pn | egrep \'^\*\' | awk \'{ print $9 }\' | tr -d \'-\''
        output = Popen(cmd, shell=True, stdout=PIPE, stderr=DEVNULL)
        offset_value_selected_source = output.communicate()[0].rstrip()
        # if offset value if empty, exiting as needs to further investigate
        if not offset_value_selected_source:
                print crit + "Collection of NTP offset was unsucessfull, please check if the ntp is operating normally!\n"
                sys.exit(1)
        if float(offset_value_selected_source) > critical_value:
                print crit + "NTP offset: " + offset_value_selected_source +  " reached its CRITICAL threshold, check ASAP!!\n"
        elif float(offset_value_selected_source) > warning_value:
                print warn + "NTP offset: " + offset_value_selected_source + " crossed it's WARNING threshold, you can take your time to check.:)\n"
        else:
                print info + "NTP offset: " + offset_value_selected_source + " is under CONTROL.\n"
        DEVNULL.close()


if __name__ == "__main__":
        platform_check()
        ntp_status_check()
