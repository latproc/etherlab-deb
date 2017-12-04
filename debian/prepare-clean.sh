#!/bin/bash

# just make sure that make distclean runs through. Without patching, etherlab screws up
# .pc is created by quilt when called by dh_quilt_patch, configure is created by bootstrap
if [ ! -d .pc -a -f configure ]; then
	dh_quilt_patch
	./configure --enable-generic --enable-debug-if --enable-cycles --enable-hrtimer --disable-e100 --disable-8139too --disable-e1000 --disable-e1000e --disable-r8169
fi
