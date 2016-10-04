SUMMARY = "Image version file"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "file://image-release"

S = "${WORKDIR}"

FILES_${PN} = "/etc/image-release"

do_install() {
	install -d ${D}/etc/
	install -m 0444 ${WORKDIR}/image-release ${D}/etc/
}
