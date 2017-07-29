#!/bin/sh

set -eu

PART_NUMBER=3

case $(mount | grep "on / ") in
/dev/mmcblk0*)
	ROOT_DEVICE="/dev/mmcblk0"
	ROOT_PARTITION="/dev/mmcblk0p$PART_NUMBER"
	;;
/dev/sda*)
	ROOT_DEVICE="/dev/sda"
	ROOT_PARTITION="/dev/sda$PART_NUMBER"
	;;
*)
	echo "Cannot determine boot device."
	exit 1
	;;
esac

START_BLOCK=$(parted $ROOT_DEVICE -ms unit s p | grep "^$PART_NUMBER" | cut -f 2 -d: | sed "s/s$//")

parted -ms $ROOT_DEVICE rm $PART_NUMBER

parted -ms $ROOT_DEVICE unit s -- mkpart primary ext3 $START_BLOCK -1

partprobe $ROOT_DEVICE
resize2fs $ROOT_PARTITION

update-rc.d -f expandfs.sh remove
