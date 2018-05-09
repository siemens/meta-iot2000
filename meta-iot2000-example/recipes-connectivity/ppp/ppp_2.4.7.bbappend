FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_remove = "file://ppp-fix-building-with-linux-4.8.patch"
SRC_URI += "file://0001-pppoe-include-netinet-in.h-before-linux-in.h.patch"
