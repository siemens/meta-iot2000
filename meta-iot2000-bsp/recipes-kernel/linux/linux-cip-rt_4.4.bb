DESCRIPTION = "Linux real-time Kernel for IOT2000 based on CIP SLTS version"
SECTION = "kernel"

require recipes-kernel/linux/linux-yocto.inc
require linux-cip_4.4.inc

FILESEXTRAPATHS_prepend := "${THISDIR}/configs:${THISDIR}/patches:"

LINUX_VERSION .= "-rt23"
SRC_URI += " \
    file://rt-0001-spi-pca2xx-pci-Allow-MSI.patch \
    file://rt-0002-gpio-dwapb-Work-around-RT-full-s-enforced-IRQ-thread.patch \
    file://defconfig \
    file://iot2000-cip-rt.scc"
SRC_URI[sha256sum] = "90d601e22edc3821048cec873696f9ccbe367a1d828418f6f429947f9499f6d6"

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
