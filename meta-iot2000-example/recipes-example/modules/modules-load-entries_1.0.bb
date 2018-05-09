LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = " \
	file://i2c-dev.conf \
	file://ofono-module.conf"

do_install() {
	install -d ${D}/etc/modules-load.d/
	install -m 0444 ${WORKDIR}/i2c-dev.conf ${D}/etc/modules-load.d/
	install -d ${D}/etc/modules-load.d/
	install -m 0444 ${WORKDIR}/ofono-module.conf ${D}/etc/modules-load.d/
}
