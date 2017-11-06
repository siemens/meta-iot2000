DESCRIPTION = "Linux Kernel for IOT2000 based on CIP SLTS version"
SECTION = "kernel"

require recipes-kernel/linux/linux-yocto.inc
require linux-cip_4.4.inc

FILESEXTRAPATHS_prepend := "${THISDIR}/configs:${THISDIR}/patches:"

SRC_URI += " \
    file://0001-spi-pxa2xx-pci-fix-ACPI-based-enumeration-of-SPI-dev.patch \
    file://0002-spi-pxa2xx-Add-support-for-GPIO-descriptor-chip-sele.patch \
    file://0003-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://0004-iot2000-hack-Adjust-pca9685-gpio-base-for-legacy-com.patch \
    file://0005-iot2000-hack-gpio-pca953x-provide-GPIO-base-based-on.patch \
    file://0006-iot2000-hack-gpio-pca953x-add-drive-property.patch \
    file://0007-iot2000-hack-pwm-pca-9685-Provide-chip-level-pwm_per.patch \
    file://defconfig"

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
