#!/bin/bash -e

# $1 is kernelversion
# $2 is path to build directory
# $3 is path to source directory
# copy symbol from build directory to $source_tree/symbols of this package
echo "Backing up masters 'Module.symvers' to 'Module.$1.symvers'."
cp $2/Module.symvers $3/Module.$1.symvers 

