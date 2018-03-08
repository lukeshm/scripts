#!/usr/bin/python
#############################################################
#
# Author : Lukesh Meshram
# Date   : 15/01/2018
# Purpose: Check-out tool after reboot/generic health-check
# Tested : Linux RHEL 5.x onwards
#
#############################################################

# Imports
from subprocess import *
import sys
import os
import shlex
import platform
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", choices=["pre", "current"],
                    help="mode of diffchecker running")
parser.add_argument("-v", help="Run the diffchecker in verbose mode",action="count")

args = parser.parse_args()

# Variable declearation
LOGDIR = '/var/tmp/diffcheck/'

# Open devnull to stderr if required

DEVNULL = open('/dev/null', 'w')

def platform_check():
        if not platform.system() == 'Linux':
                print "Non supported OS platform, please try it on Linux only, eixiting."
                sys.exit(1)
# Define Dictonary : command + value

ALL_RESOURCES = {
        "CMD_rpm" : "/usr/bin/rpm -qa | sort",
        "CMD_ip_a_s" : "/usr/sbin/ip a s",
        "CMD_kernel" : "/usr/bin/uname -r",
        "CMD_CPU" : "cat /proc/cpuinfo  | grep processor",
        "CMD_memory" : "/usr/bin/egrep 'MemTotal' /proc/meminfo | awk '{print $2}'",
        "CMD_df" : "/usr/bin/df -hP | awk '{ print $6 }' | egrep -v Mounted",
        "CMD_disk" : "/usr/sbin/fdisk -l | grep Disk | egrep -v 'Disk label type|identifier|mapper'",
        "CMD_processes" : "/usr/bin/ps -ef | egrep 'docker|httpd|crond'",
        "CMD_routes" : "/usr/bin/netstat -nr",
                }

nothing = os.system('clear')

# Function to create pre status of components (will be collecting vai cron)

def collect_data(stage):
        # Creating DIR for logs
        if not os.path.exists(LOGDIR):
                os.makedirs(LOGDIR)
        # Loop to collect all pre/post date
        for key, value in ALL_RESOURCES.items():
                try:
                        filename = LOGDIR + key + "." + stage
                        with open(filename, 'w') as f:
                                Popen(shlex.split(value), stdout=f, stderr=DEVNULL).communicate()[0]
                except IOError:
                        print("IO error occured, please try again.")
                        sys.exit(1)

# Compair the pre against current state and use sdiff

def sdiff_fuction():
        if os.path.exists(LOGDIR):
                for key, value in ALL_RESOURCES.items():
                        filename_pre = LOGDIR + key + "." + 'pre'
                        filename_current = LOGDIR + key + "." + 'current'
                        if os.path.isfile(filename_pre):
                                collect_data('current')
                                global CMD_sdiff
                                CMD_sdiff = '/usr/bin/sdiff -s -w 150 ' + filename_pre + " " + filename_current
                                if call(CMD_sdiff, shell=True, stdout=DEVNULL,stderr=DEVNULL) == 1:
                                        print '{0: <25}'.format(key) + "NOT OK"
                                        verbose_fun()
                                else:
                                        print '{0: <25}'.format(key) + "OK"


def verbose_fun():
        if args.v >= 1:
                print "Pre output \t\t\t\t\t\t\t\t  | Current output"
                verbose_output = Popen(CMD_sdiff, shell=True, stderr=DEVNULL).communicate()[0]
                print verbose_output


if __name__ == "__main__":
        platform_check()
        if args.c == "pre":
                collect_data('pre')
        else:
                sdiff_fuction()
