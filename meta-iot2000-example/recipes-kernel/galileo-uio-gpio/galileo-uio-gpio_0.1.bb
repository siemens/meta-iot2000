SUMMARY = "Crude UIO driver for the Galileo to map GPIO registers into userspace"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

SRC_URI = "file://Makefile \
           file://galileo-uio-gpio.c \
           file://COPYING \
          "

S = "${WORKDIR}"

do_install_append() {
	install -d ${D}${sysconfdir}/modules-load.d
	echo "galileo-uio-gpio" > ${D}${sysconfdir}/modules-load.d/galileo-uio-gpio.conf
}

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.
