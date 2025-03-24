#This recipe modifies the default settings of busybox
#arp.cfg adds the "arp" command

FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI += "file://arp.cfg"
SRC_URI += "file://lsusb.cfg"
SRC_URI += "file://nc.cfg"
SRC_URI += "file://ntpclient.cfg"
SRC_URI += "file://ntp.conf"
SRC_URI += "file://ntpd.busybox"
SRC_URI += "file://no-ext-dhcp.cfg"

PACKAGES =+ "${PN}-ntpd"

INITSCRIPT_PACKAGES += "${PN}-ntpd"
INITSCRIPT_NAME:${PN}-ntpd = "ntpd.busybox"

FILES:${PN}-ntpd = "${sysconfdir}/init.d/ntpd.busybox ${sysconfdir}/ntp.conf"

CONFFILES:${PN}-ntpd = "${sysconfdir}/ntp.conf"

RRECOMMENDS:${PN} += "${PN}-ntpd"

do_install:append() {
	install -d ${D}${sysconfdir}
	install -m 0644 ${WORKDIR}/ntp.conf ${D}${sysconfdir}/

	install -d ${D}${sysconfdir}/init.d
	install -m 0755 ${WORKDIR}/ntpd.busybox ${D}${sysconfdir}/init.d/
}
