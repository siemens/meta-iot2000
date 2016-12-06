SUMMARY = "Copy iot2000setup files to file system"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "file://expandfs.sh file://iot2000setup.py"

FILES_${PN} += " \
	${sysconfdir}/iot2000setup/expandfs.sh \
	${sysconfdir}/iot2000setup/iot2000setup.py \
	${bindir}/iot2000setup \
"

RDEPENDS_${PN} += " libnewt-python"

do_install() {
   install -d ${D}${sysconfdir}/iot2000setup
   install -d ${D}${bindir}
   install -m 0755 ${WORKDIR}/expandfs.sh ${D}${sysconfdir}/iot2000setup/expandfs.sh
   install -m 0755 ${WORKDIR}/iot2000setup.py ${D}${sysconfdir}/iot2000setup/iot2000setup.py
   ln -sf /etc/iot2000setup/iot2000setup.py ${D}${bindir}/iot2000setup
}


