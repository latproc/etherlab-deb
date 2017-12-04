#!/bin/bash

# $1 is kernelversion
# $2 is dkms_tree
# $3 is module_version
# $4 is module
# $5 is suffix

# copy symbol from build directory to $source_tree/symbols of this package
echo "Fetching masters 'Module.$1.symvers'"
cp $2/etherlab_core$5/$3/source/symbols/Module.$1.symvers \
	$2/$4/$3/build/symbols
