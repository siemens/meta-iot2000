SUMMARY = "Register spidev userspace driver with SPI channel 1"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

SRC_URI = "file://Makefile \
           file://galileo-spi1-spidev.c \
           file://COPYING \
          "

S = "${WORKDIR}"

do_install_append() {
            install -d ${D}${sysconfdir}/modules-load.d
            echo "galileo-spi1-spidev" > ${D}${sysconfdir}/modules-load.d/galileo-spi1-spidev.conf
}

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.
