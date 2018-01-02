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
SRCREV = "6c97018d1d4626e21b5233eb28e607e412c79ebe"
LINUX_VERSION .= "-rt10"

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
