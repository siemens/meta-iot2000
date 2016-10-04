SUMMARY = "Fake a platform driver module GalileoGen2 for Arduino sketches"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

SRC_URI = "file://Makefile \
           file://galileogen2-fake.c \
           file://COPYING \
          "

S = "${WORKDIR}"

do_install_append() {
            install -d ${D}${sysconfdir}/modules-load.d
            echo "galileogen2-fake" > ${D}${sysconfdir}/modules-load.d/galileogen2-fake.conf
}

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.
