#!/usr/bin/env python

import sys
import os
import os.path as osp
import subprocess

def subst(filename, substList):
	with open(filename[0:-3], 'w') as outFile:
		sedCmd = ['sed']
		for s in substList:
			sedCmd.extend(['-e', s])
		sedCmd.append(filename)
		subprocess.call(sedCmd, stdout=outFile)
	os.chmod(filename[0:-3], os.stat(filename).st_mode)

def delete(filename):
	delFile = filename[0:-3]
	if osp.exists(delFile):
		os.remove(delFile)

def main():
	if len(sys.argv) < 3:
		print "ERR: expected <subst|del> <filename> [<sed -e params>]"
		return 1
	if not sys.argv[2].endswith('.in'):
		print "ERR: '{0}' does not end with .in".format(sys.argv[2])
		return 1

	if sys.argv[1] == "subst":
		subst(sys.argv[2], sys.argv[3:])
	elif sys.argv[1] == "del":
		delete(sys.argv[2])
	else:
		print "ERR: '{0}' must be subst or del".format(sys.argv[1])
		return 1
	return 0

if __name__ == "__main__":
	sys.exit(main())
