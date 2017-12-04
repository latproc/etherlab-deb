#!/bin/bash
# This script will create a version number for etherlab based on the current
# repository version and add it to the changelog.

CommitDate="$(hg parents --template '{date|shortdate}' | awk -F"-" '{ print $1$2$3 }')"
CommitRev="$(hg parents --template '{rev}')"

dch --newversion "$CommitDate+$CommitRev-1" --preserve --changelog debian/changelog

