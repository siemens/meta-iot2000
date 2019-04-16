LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

LINUX_VERSION = "4.4.176-cip31"
SRC_URI = " \
    https://git.kernel.org/pub/scm/linux/kernel/git/cip/linux-cip.git/snapshot/linux-cip-${LINUX_VERSION}.tar.gz"
SRC_URI[sha256sum] = "14fa6a7f08859848faae819fb7c025a8c96f18f5a208ceb3fc25a6e276bd7f69"

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

S = "${WORKDIR}/linux-cip-${LINUX_VERSION}"
