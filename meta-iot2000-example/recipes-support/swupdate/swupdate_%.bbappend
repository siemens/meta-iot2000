FILESEXTRAPATHS_prepend := "${THISDIR}/swupdate:"

SRC_URI += " \
    file://swupdate_handlers.lua \
    file://tools_makefile.patch \
    file://progress_firmware.c \
    file://swupdate.cfg"

FILES_${PN} += "/etc/swupdate.cfg /usr/bin/progress_firmware"

DEPENDS += "efibootguard"

INHIBIT_UPDATERCD_BBCLASS = "1"

do_configure_prepend () {
    cp ${WORKDIR}/swupdate_handlers.lua ${S}
    cp ${WORKDIR}/progress_firmware.c ${S}/tools/progress_firmware.c
}

# bitbake complains because progress_firmware is already stripped which would prevent
# debugging. To prevent this QA error:
INSANE_SKIP_${PN}_append = " already-stripped"

do_install_append() {
    install -d ${D}${sysconfdir}
    install -m 644 ${WORKDIR}/swupdate.cfg ${D}${sysconfdir}/swupdate.cfg
    install -m 755 ${S}/tools/progress_firmware ${D}/usr/bin/progress_firmware
}
