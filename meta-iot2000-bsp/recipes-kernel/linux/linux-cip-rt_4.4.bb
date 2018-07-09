DESCRIPTION = "Linux real-time Kernel for IOT2000 based on CIP SLTS version"
SECTION = "kernel"

require recipes-kernel/linux/linux-yocto.inc
require linux-cip_4.4.inc

FILESEXTRAPATHS_prepend := "${THISDIR}/configs:${THISDIR}/patches:"

SRC_URI = " \
    git://git.kernel.org/pub/scm/linux/kernel/git/wagi/linux-cip-rt.git;branch=linux-4.4.y-cip-rt;protocol=https \
    ${KERNEL_PATCHES} \
    file://rt-0001-spi-pca2xx-pci-Allow-MSI.patch \
    file://rt-0002-gpio-dwapb-Work-around-RT-full-s-enforced-IRQ-thread.patch \
    file://defconfig \
    file://iot2000-cip-rt.scc"
SRCREV = "e5981d0d0add6277de1ddc94cf67e78a9557aea4"
LINUX_VERSION .= "-rt19"

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
