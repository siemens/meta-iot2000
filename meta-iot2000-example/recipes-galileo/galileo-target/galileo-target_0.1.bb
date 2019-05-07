DESCRIPTION = "Clanton Software Sketch Framework"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=b234ee4d69f5fce4486a80fdaf4a4263"

SRC_URI = "file://galileo-target \
           file://launcher.sh \
           file://galileod.init \
           file://galileo-target.service \
           file://galileo-sketch-reset.service \
           file://r1_2_sketch_reset.patch"

INSTALLDIR = "/opt/cln/galileo"
FILES_${PN} += "${INSTALLDIR} \
                ${systemd_unitdir}/system/ \
                /sketch"
FILES_${PN}-dbg += "${INSTALLDIR}/.debug"

S = "${WORKDIR}/galileo-target"

RDEPENDS_${PN} += "uclibc uclibc-libpthread uclibc-libm uclibc-binlibs"
RDEPENDS_${PN} += "galileogen2-fake galileo-uio-gpio galileo-spi1-spidev"
RDEPENDS_${PN} += "acm-gadget"

do_compile() {
	make
}

do_install() {
        oe_runmake install DESTDIR=${D}/

        install -d ${D}${INSTALLDIR}
        install -m 0755 ${WORKDIR}/launcher.sh ${D}${INSTALLDIR}/

        install -d ${D}${sysconfdir}/init.d
        install -m 0755 ${WORKDIR}/galileod.init ${D}${sysconfdir}/init.d/galileod

        install -d ${D}${systemd_unitdir}/system
        install -m 0644 ${WORKDIR}/galileo-target.service ${D}${systemd_unitdir}/system/
        install -m 0644 ${WORKDIR}/galileo-sketch-reset.service ${D}${systemd_unitdir}/system/

        install -d ${D}${base_libdir}/udev/rules.d
        echo 'SUBSYSTEM=="spidev", SYMLINK+="spidev1.0"' > ${D}${base_libdir}/udev/rules.d/99-galileo-arduino-spi-compat.rules

        install -d ${D}/sketch
}

inherit update-rc.d
INITSCRIPT_PACKAGES = "${PN}"
INITSCRIPT_NAME = "galileod"

inherit systemd
SYSTEMD_SERVICE_${PN} = "galileo-target.service galileo-sketch-reset.service"
