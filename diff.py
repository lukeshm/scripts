#!/usr/bin/python

from subprocess import *
import sys
import os

import platform

if not platform.system() == 'Linux':
	print "Non supported OS platform, please try it on Linux only, eixiting."
	sys.exit(1)

# CMDS
CMD_rpm = '/usr/bin/rpm -qa | sort'
CMD_ip_a_s = '/usr/sbin/ip a s'
CMD_kernel = 'platform.kernel()'
CMD_CPU = 'cat /proc/cpuinfo  | grep processor'
CMD_memory = '/usr/bin/egrep 'MemTotal' /proc/meminfo | awk '{print $2}''
CMD_df = '/usr/bin/df -hP | awk '{ print $6 }' | egrep -v Mounted'
CMD_disk = '/usr/sbin/fdisk -l | grep Disk | egrep -v 'Disk label type|identifier|mapper''
CMD_processes = '/usr/bin/ps -ef | egrep 'docker|httpd|crond''
CMD_routes = '/usr/bin/netstat -nr'


