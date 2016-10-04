#This recipe modifies the default settings of busybox
#arp.cfg adds the "arp" command

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " file://arp.cfg"
