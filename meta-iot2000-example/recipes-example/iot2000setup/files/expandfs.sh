#!/bin/sh

set -eu

DEVICE_TYPE=$(mount | head -n1 | cut -f 1 -d ' ' | cut -f 3 -d / | head -c 1) # returns 's' for boot from USB, 'm' for boot from SD

if [ $DEVICE_TYPE == "s" ]
	then
		ROOT_PARTITION="/dev/sda2"
		ROOT_DEVICE="/dev/sda"
		PART_NUMBER=2 
	elif [ $DEVICE_TYPE=="m" ]
		then
			ROOT_PARTITION="/dev/mmcblk0p2"
			ROOT_DEVICE="/dev/mmcblk0"
			PART_NUMBER=2 
	else
		echo "Cannot determine boot device."
		exit 1
fi


START_BLOCK=$(parted $ROOT_DEVICE -ms unit s p | grep "^2" | cut -f 2 -d: | rev | cut -c 2- | rev)

parted -ms $ROOT_DEVICE rm $PART_NUMBER

parted -ms $ROOT_DEVICE unit s -- mkpart primary ext4 $START_BLOCK -1

partprobe $ROOT_DEVICE
resize2fs $ROOT_PARTITION

exit 0
