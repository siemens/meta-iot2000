#!/bin/sh

THIS_SCRIPT="$(basename $0)"

log () {
	echo ${THIS_SCRIPT}: $1 > /dev/kmsg
}

disable () {
	log "Deactivating this automatic resizer"
	update-rc.d -f expandfs.sh remove
}

ROOT_DEVICE=$(findmnt / -o source -n | sed 's/p\?[0-9]*$//')
LAST_PART=$(sfdisk -d ${ROOT_DEVICE} | tail -1 | awk '{print $1}')

log "Unmounting last partition"
umount -f $LAST_PART > /dev/null

log "Resizing last partition"
sfdisk -d ${ROOT_DEVICE} 2>/dev/null | grep -v last-lba | \
	sed 's|\('${LAST_PART}' .*, \)size=[^,]*, |\1|' | \
	sfdisk --force ${ROOT_DEVICE} 2>&1 | logger -t ${THIS_SCRIPT}

log "Informing kernel about new partitioning"
partprobe > /dev/null

log "Resizing file system"
resize2fs ${LAST_PART} 2>&1 | logger -t ${THIS_SCRIPT}

log "Disabling this init script"
disable

log "Remounting last partition"
mount $LAST_PART > /dev/null
