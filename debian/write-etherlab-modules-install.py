#!/usr/bin/env python
"""Writes the dh_install file for etherlab-modules{suffix}.install.

As convention, this script must not create/copy files into the debian directories. It
MUST only write the dh_install files and do the pattern substitution as required. If
files need to be customized (e.g. substitute package version in dkms.conf), we need to
create this file somewhere from a template before we run dh_install. This script should
then just produce the line that is required to install the substituted file into target.
"""

import os
import os.path as osp
import sys

# This are files that every driver needs in a format suitable for
# automatically creating the entries for dh_install.
DRIVER_REQUIRED_FILES = [
	('devices/ecdev.h', 'devices')
	,('globals.h', '')
	,('revision', '')
	,('include/*.h', 'include')
	,('debian/dkms/get-symbols.sh', '')
	,('debian/dkms/Kbuild', '')
]

class Driver(object):
	def __init__(self, name, hasSubdir):
		self.driverName = name
		self.hasSubdir = hasSubdir

DRIVERS = [
	Driver('e1000e', True)
	,Driver('e1000', True)
	,Driver('8139too', False)
	,Driver('r8169', False)
]

def	writeDhInstallEntries(installFile, driver, suffix, version):
	# delimiting between version and name is exectly oposite in dkms and debian (- vs _)
	targetPath = 'usr/src/etherlab_{0}{1}'.format(driver.driverName, suffix).replace('-', '_')
	targetPath += '-' + version + '/'
	installFile.write('\n# section for ' + driver.driverName + '\n')
	if driver.hasSubdir:
		# Code files for the driver
		sourceFiles = 'devices/{0}/*-ethercat.*'.format(driver.driverName)
		targetFiles = targetPath + 'devices/' + driver.driverName
		installFile.write('{0} {1}\n'.format(sourceFiles, targetFiles))

		# Kbuild files for the driver
		source = 'debian/dkms/{0}/'.format(driver.driverName)
		installFile.write('{0}/devices/Kbuild {1}/devices/\n'.format(source, targetPath))
		installFile.write('{0}/Kbuild {1}/devices/{2}\n'.format(source, targetPath, driver.driverName))
	else:
		# code files for the driver
		sourceFiles = 'devices/{0}-*-ethercat.*'.format(driver.driverName)
		targetFiles = targetPath + 'devices/'
		installFile.write('{0} {1}\n'.format(sourceFiles, targetFiles))

		# Kbuild files for the driver
		source = 'debian/dkms/{0}/'.format(driver.driverName)
		installFile.write('debian/dkms/{0}/Kbuild {1}/devices/{0}\n'.format(driver.driverName, targetPath))


	# This files are copied and required by every driver
	for source, destAppend in DRIVER_REQUIRED_FILES:
		installFile.write('{0} {1}{2}\n'.format(source, targetPath, destAppend))

	installFile.write('debian/dkms/{0}/dkms.conf {1}\n'.format(driver.driverName, targetPath))

def main():
	if len(sys.argv) < 3:
		print "ERR: Not enough arguments: expected <package-suffix> <package-version>"
		return 1

	pkgVersion = sys.argv[2]
	pkgSuffix = sys.argv[1]

	installFile = open('debian/etherlab-modules{0}-dkms.install'.format(pkgSuffix), 'a')

	for d in DRIVERS:
		writeDhInstallEntries(installFile, d, pkgSuffix, pkgVersion)
	return 0


if __name__ == "__main__":
	sys.exit(main())
