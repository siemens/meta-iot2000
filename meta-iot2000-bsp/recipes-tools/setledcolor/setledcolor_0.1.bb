DESCRIPTION = "This installs a small python script to handle the led color for the SIMATIC IOT2040"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "file://setledcolor.py"

S = "${WORKDIR}"

FILES_${PN} += "${sysconfdir}/setledcolor/setledcolor.py \
				${bindir}/setledcolor"

do_install() {
	install -d ${D}${sysconfdir}/setledcolor
	install -d ${D}${bindir}
	install -m 755 ${WORKDIR}/setledcolor.py ${D}${sysconfdir}/setledcolor/
	ln -sf /etc/setledcolor/setledcolor.py ${D}${bindir}/setledcolor
}
