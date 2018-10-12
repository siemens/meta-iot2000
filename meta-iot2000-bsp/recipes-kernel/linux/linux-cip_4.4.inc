LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

SRC_URI = " \
    git://git.kernel.org/pub/scm/linux/kernel/git/bwh/linux-cip;protocol=https"
SRCREV = "5dcb70a7e56e2c00e1c8ca593c61e378cef22f51"
LINUX_VERSION = "4.4.154-cip28"

KERNEL_PATCHES = " \
    file://0001-stmmac-pci-Make-stmmac_pci_info-structure-constant.patch \
    file://0002-stmmac-pci-Use-stmmac_pci_info-for-all-devices.patch \
    file://0003-stmmac-pci-Make-stmmac_pci_find_phy_addr-truly-gener.patch \
    file://0004-stmmac-pci-Select-quark_pci_dmi_data-from-quark_defa.patch \
    file://0005-stmmac-pci-Use-dmi_system_id-table-for-retrieving-PH.patch \
    file://0006-stmmac-pci-Adjust-IOT2000-matching.patch \
    file://0007-serial-8250_exar-Adjust-IOT2000-matching.patch \
    file://0008-mfd-intel_quark_i2c_gpio-Adjust-IOT2000-matching.patch \
    file://0009-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://0010-iot2000-hack-Adjust-pca9685-gpio-base-for-legacy-com.patch \
    file://0011-iot2000-hack-gpio-pca953x-provide-GPIO-base-based-on.patch \
    file://0012-iot2000-hack-gpio-pca953x-add-drive-property.patch \
    file://0013-iot2000-hack-pwm-pca-9685-Provide-chip-level-pwm_per.patch"

S = "${WORKDIR}/git"
