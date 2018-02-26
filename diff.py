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

# nothing = os.system('clear')

# Function to create pre status of components (will be collecting vai cron)

def collect_data(stage):
	# Creating DIR for logs
	#os.mkdir(LOGDIR)
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
				CMD_sdiff = '/usr/bin/sdiff -s -w 200 ' + filename_pre + " " + filename_current
				if call(CMD_sdiff, shell=True, stdout=DEVNULL,stderr=DEVNULL) == 1:
					print key + "\t\t\t\t\t" + "NOT OK"
				else:
					print key + "\t\t\t\t\t" + "    OK"



if __name__ == "__main__":
	platform_check()
	collect_data('pre')
	sdiff_fuction()
