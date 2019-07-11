SUMMARY = "A visual tool for wiring the Internet of Things"
HOMEPAGE = "http://nodered.org"

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "Apache-2.0 & ISC & BSD-2-Clause & BSD & EUPL-1.1 & BSD-3-Clause & MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d6f37569f5013072e9490d2194d10ae6"

inherit npm-ng

SRC_URI += "file://node-red.init"

do_install_append() {
    install -d ${D}${sysconfdir}/init.d
    install -m 0755 ${WORKDIR}/node-red.init ${D}${sysconfdir}/init.d/node-red
}

FILES_${PN} += "${sysconfdir}/init.d/node-red.sh ${bindir}/node-red"

RDEPENDS_${PN} += "python bash"

INSANE_SKIP_${PN} += "textrel"
