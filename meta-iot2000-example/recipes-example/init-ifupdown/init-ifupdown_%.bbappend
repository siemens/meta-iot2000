#This recipe will provide a default confi for networking.
#The default configuration provided with this recipe is both ports using dhcp.
#If you wish to change this behavior, simply modify the file "interfaces" 
#according to your requirements. This file will be placed at 
#/etc/network/interfaces.

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " file://interfaces"
