DESCRIPTION = "Tool to switch between the com port modes"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "file://switchmode.c"

S = "${WORKDIR}"
INSTDIR = "/usr/bin/"

FILES_${PN} = "${INSTDIR}*"

do_compile() {
	${CC} ${CFLAGS} ${LDFLAGS} ${WORKDIR}/switchmode.c -o switchserialmode
}

do_install() {
	install -d ${D}${INSTDIR}
	install -m 755 ${WORKDIR}/switchserialmode ${D}${INSTDIR}
}
