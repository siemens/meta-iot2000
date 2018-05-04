DESCRIPTION = "Linux Kernel for IOT2000 using latest mainline kernel"
SECTION = "kernel"

include recipes-kernel/linux/linux-yocto.inc

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=bbea815ee2795b2f4230826c0c6b8814"

FILESEXTRAPATHS_prepend := "${THISDIR}/configs:${THISDIR}/patches:"

SRC_URI = " \
    git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git;protocol=https \
    file://0001-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://defconfig \
    file://iot2000-mainline.scc"

SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git"

COMPATIBLE_MACHINE = "iot2000"
KMACHINE = "intel-quark"

# This recipe is tracking always the latest version
do_kernel_version_sanity_check() {
}
