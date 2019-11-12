DESCRIPTION = "Linux real-time Kernel for IOT2000 based on CIP SLTS version"
SECTION = "kernel"

require recipes-kernel/linux/linux-yocto.inc
require linux-cip_4.4.inc

LINUX_VERSION = "4.4.190-cip36-rt25"
SRC_URI += " \
    file://rt-0001-spi-pca2xx-pci-Allow-MSI.patch \
    file://rt-0002-gpio-dwapb-Work-around-RT-full-s-enforced-IRQ-thread.patch \
    file://iot2000-cip-rt.scc"
SRC_URI[sha256sum] = "7fe6c2bd0b61ac3a5b71f9078608afb4eef8a565f70cbb34fa9b35a3fa001177"

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
