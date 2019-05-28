SUMMARY = "A Node-RED node to talk to an Intel Galileo or Edison using mraa"

LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://hardware/intel/LICENSE;md5=2c0cb74248cfa16e787ab1cf4c16e94e"

SRC_URI = "git://github.com/node-red/node-red-nodes;protocol=https \
    file://0001-intel-gpio-HTML-cleanups.patch \
    file://0002-intel-gpio-Consistently-use-this-where-available.patch \
    file://0003-intel-gpio-Add-support-for-initial-message-from-digi.patch \
    file://0004-intel-gpio-Use-isrExit-in-favor-of-isr-m.EDGE_BOTH-n.patch \
    file://0005-intel-gpio-Add-polling-of-input-pins-in-absence-of-i.patch \
    file://0006-intel-gpio-Respect-user-defined-name-for-output-pin-.patch \
    file://0007-intel-gpio-Mark-output-pin-13-as-LED-on-Galileo-v2.patch \
    file://0008-intel-gpio-Add-support-for-user-button-on-Galileo-v2.patch \
    file://0009-intel-gpio-Add-IOT2020-and-IOT2040-board-detection.patch \
    file://0010-intel-gpio-Add-support-for-red-LED-of-IOT2040.patch \
    file://0011-intel-gpio-Privatize-version.patch"
SRCREV = "8d45e85acfa10b53fb94b1d6bfc16b9f8cc39eea"

S = "${WORKDIR}/git"

NODE_MODULES_DIR = "/home/root/.node-red/node_modules"

do_install() {
    install -d ${D}${NODE_MODULES_DIR}/${PN}
    install -m 0644 ${S}/hardware/intel/* ${D}${NODE_MODULES_DIR}/${PN}
}

FILES_${PN} = "${NODE_MODULES_DIR}/${PN}"
