#!/usr/bin/python

from subprocess import *
import sys
import os
import shlex
import platform

DEVNULL = open('/dev/null', 'w')

if not platform.system() == 'Linux':
	print "Non supported OS platform, please try it on Linux only, eixiting."
	sys.exit(1)

LOGDIR = '/var/tmp/diffcheck/'

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

def collect_data(stage):
	# Creating DIR for logs
	os.mkdir(LOGDIR)
	# Loop to collect all pre/post date
	for key, value in ALL_RESOURCES.items():
		try:
			filename = LOGDIR + key + "." + stage
        		with open(filename, 'w') as f:
            			subprocess.Popen(shlex.split(value), stdout=f, stderr=DEVNULL).communicate()[0]
		except IOError:
			print("IO error occured, please try again.")
			sys.exit(1)


def sdiff_fuction:
	if os.direxists(LOGDIR):
		for key, value in ALL_RESOURCES.items():
			filename_pre = LOGDIR + key + "." + pre
			filename_current = LOGDIR + key + "." + current
			if os.path.isfile(filename_pre):
				collect_data(current)
				CMD_sdiff = '/usr/bin/sdiff -s -w 200 ' + filename_pre + " " + filename_current
				subprocess.Popen("
				
	
	

