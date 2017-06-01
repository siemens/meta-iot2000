#This recipe modifies the default settings of busybox
#arp.cfg adds the "arp" command

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " file://arp.cfg"
SRC_URI_append = " file://lsusb.cfg"
SRC_URI_append = " file://ntpclient.cfg"
SRC_URI_append = " file://ntp.conf"
SRC_URI_append = " file://ntpd.busybox"

inherit update-rc.d

INITSCRIPT_PACKAGES = "${PN}"
INITSCRIPT_NAME = "ntpd.busybox"

RDEPENDS_${PN} += "tzdata"

do_install_append() {
	install -d ${D}${sysconfdir}
	install -m 0644 ${WORKDIR}/ntp.conf ${D}${sysconfdir}/

	install -d ${D}${sysconfdir}/init.d
	install -m 0755 ${WORKDIR}/ntpd.busybox ${D}${sysconfdir}/init.d/
}
