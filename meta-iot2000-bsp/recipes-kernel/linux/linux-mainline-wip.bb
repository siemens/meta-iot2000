DESCRIPTION = "Linux Kernel for IOT2000 using a mainline patch queue"
SECTION = "kernel"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

inherit kernel
require recipes-kernel/linux/linux-yocto-iot2000.inc

KMETA = "kernel-meta"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI = " \
    git://github.com/siemens/linux.git;branch=queues/iot2000;protocol=https \
    git://git.yoctoproject.org/git/yocto-kernel-cache;type=kmeta;name=meta;branch=master;destsuffix=${KMETA};protocol=https \
    file://iot2000.scc"
SRCREV = "${AUTOREV}"
SRCREV_meta = "${AUTOREV}"

S = "${WORKDIR}/git"

COMPATIBLE_MACHINE = "iot2000"
KMACHINE = "intel-quark"

# This recipe is tracking always the latest version
do_kernel_version_sanity_check() {
}
