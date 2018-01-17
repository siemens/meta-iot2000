SUMMARY = "Copy iot2000setup files to file system"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

inherit update-rc.d

SRC_URI = "file://expandfs.sh file://iot2000setup.py"

FILES_${PN} += " \
	${sysconfdir}/init.d/expandfs.sh \
	${bindir}/iot2000setup \
"

RDEPENDS_${PN} += "libnewt-python python3-mraa util-linux-sfdisk"
INITSCRIPT_NAME = "expandfs.sh"
INITSCRIPT_PARAMS = "defaults 10"

do_install() {
   install -d ${D}${sysconfdir}/init.d
   install -d ${D}${bindir}
   install -m 0755 ${WORKDIR}/iot2000setup.py ${D}${bindir}/iot2000setup
   install -m 0755 ${WORKDIR}/expandfs.sh ${D}${sysconfdir}/init.d/expandfs.sh
}
