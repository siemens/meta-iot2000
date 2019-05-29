#!/bin/sh

LOG_CMD="logger -t expandfs.sh"

disable_hint() {
	echo
	echo "Please note: This script is not disabled."
	echo "To disable it, use:"
	echo
	echo "update-rc.d -f expandfs.sh remove"
}

ROOT_DEVICE=$( { findmnt / -o source -n || echo "ERR"; } | sed 's/p\?[0-9]*$//' 2>/dev/null )
RES=$( echo "${ROOT_DEVICE}" | tail -1 )
if [ "${RES}" = "ERR" ]; then
	echo "ERROR: could not find root device." | ${LOG_CMD}
	disable_hint
	exit 1
fi

CURRENT_TABLE="$( sfdisk -d ${ROOT_DEVICE} || echo ERR )"
RES=$( echo "${CURRENT_TABLE}" | tail -1 )
if [ "${RES}" = "ERR" ]; then
	echo "ERROR: could not read partition table." | ${LOG_CMD}
	disable_hint
	exit 1
fi

LAST_PART=$( echo "${CURRENT_TABLE}" | awk 'END{print $1}' )
echo "Resizing "${LAST_PART} | ${LOG_CMD}

RES=$( { echo "${CURRENT_TABLE}" | grep -v last-lba | \
	sed "\#\(${LAST_PART}\)#s#\(size=\)\s*[0-9]*,##" | \
	sfdisk --force "${ROOT_DEVICE}"; } 2>&1 || echo "ERR" )
echo "${RES}" | ${LOG_CMD}

RES=$( echo "${RES}" | tail -1 )
if [ "${RES}" = "ERR" ]; then
	echo "ERROR: could not update partition table." | ${LOG_CMD}
	disable_hint
	exit 1
fi

echo "Informing kernel about new partitioning" | ${LOG_CMD}
partprobe > /dev/null

echo "Online-Resizing file system" | ${LOG_CMD}
RES=$( resize2fs ${LAST_PART} 2>&1 || echo "ERR" )
echo ${RES} | ${LOG_CMD}

RES=$( echo "${RES}" | tail -1 )
if [ "${RES}" = "ERR" ]; then
	echo "ERROR: could not resize file system" | ${LOG_CMD}
	disable_hint
	exit 1
fi

echo "Deactivating this automatic resizer" | ${LOG_CMD}
update-rc.d -f expandfs.sh remove
