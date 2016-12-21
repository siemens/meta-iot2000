DESCRIPTION = "includes the firmware files for broadcom and realtek wifi devices"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

SRC_URI = "git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git"
SRCREV = "a179db97914da5e650c21ba8f9b0bae04a0f8a41"
S = "${WORKDIR}"
INSTDIR = "/lib/firmware/"

FILES_${PN} = "${INSTDIR}*"

do_install() {
	install -d ${D}${INSTDIR}
	install -d ${D}${INSTDIR}brcm/
	install -d ${D}${INSTDIR}rtlwifi/
	cp -R ${S}/git/brcm/* ${D}${INSTDIR}brcm/
	cp -R ${S}/git/rtlwifi/* ${D}${INSTDIR}rtlwifi/
}
