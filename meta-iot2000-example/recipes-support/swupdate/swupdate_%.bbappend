FILESEXTRAPATHS_prepend := "${THISDIR}/swupdate:"

SRCREV = "012374087c747f05216a7f002e4b8a34bc142c52"

SRC_URI += "file://swupdate_handlers.lua"
SRC_URI += "file://Makefile"
SRC_URI += "file://progress_firmware.c"
SRC_URI += "file://swupdate.cfg"

FILES_${PN} += "/etc/swupdate.cfg /usr/bin/progress_firmware"

DEPENDS += "efibootguard"

do_configure_prepend () {
        cp ${WORKDIR}/swupdate_handlers.lua ${S}
        cp ${WORKDIR}/Makefile ${S}/tools/Makefile
        cp ${WORKDIR}/progress_firmware.c ${S}/tools/progress_firmware.c
}

do_install_append() {
        install -d ${D}${sysconfdir}
        install -m 644 ${WORKDIR}/swupdate.cfg ${D}${sysconfdir}/swupdate.cfg
        install -m 755 ${S}/tools/progress_firmware_unstripped ${D}/usr/bin/progress_firmware
}
