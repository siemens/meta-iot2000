#!/bin/sh

set -eu

THIS_SCRIPT="$(basename $0)"

log () {
	echo ${THIS_SCRIPT}: $1 > /dev/kmsg
}

disable () {
	log "Deactivating this automatic resizer"
	update-rc.d -f expandfs.sh remove
}

case $(mount | grep "on / ") in
/dev/mmcblk0*)
	ROOT_DEVICE="/dev/mmcblk0"
	EXPAND_PARTITION="/dev/mmcblk0p"
	;;
/dev/sda*)
	ROOT_DEVICE="/dev/sda"
	EXPAND_PARTITION="/dev/sda"
	;;
*)
	log "Cannot determine root device."
	disable
	exit 1
	;;
esac

log "Fixing backup GPT position"
parted ${ROOT_DEVICE} print Fix

LAST_PART="$(parted ${ROOT_DEVICE} -ms unit s p | tail -n 1 | cut -d ':' -f 1)"
if [ "x${LAST_PART}" == "x" ]
then
	log "Cannot find last partition of root device."
	disable
	exit 1
fi

EXPAND_PARTITION="${EXPAND_PARTITION}${LAST_PART}"

MAXSIZE="$(parted ${ROOT_DEVICE} -s unit MB print list | grep Disk | cut -d' ' -f 3 | tr -d MB)"
if [ "x${MAXSIZE}" == "x" ]
then
	log "Error obtaining maximum partition size"
	disable
	exit 1
fi

log "Resizing ${EXPAND_PARTITION} to maximum"
parted ${ROOT_DEVICE} -s resizepart ${LAST_PART} ${MAXSIZE}M
res=$?
if [ $res -ne 0 ]
then
	log "Error resizing partition"
	disable
	exit 1
fi

partprobe ${ROOT_DEVICE}

log "Resizing file system on ${EXPAND_PARTITION}"
resize2fs ${EXPAND_PARTITION}
res=$?
if [ $res -ne 0 ]
then
	log "Error resizing file system"
	disable
	exit 1
fi

disable
