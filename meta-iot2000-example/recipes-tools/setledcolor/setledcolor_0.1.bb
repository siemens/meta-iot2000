DESCRIPTION = "This installs a small python script to handle the led color for the SIMATIC IOT2040"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "file://setledcolor.py"

S = "${WORKDIR}"

FILES_${PN} += "${bindir}/setledcolor.py"

RDEPENDS_${PN} = "python3-mraa"

do_install() {
	install -d ${D}${bindir}
	install -m 755 ${WORKDIR}/setledcolor.py ${D}${bindir}/
}
