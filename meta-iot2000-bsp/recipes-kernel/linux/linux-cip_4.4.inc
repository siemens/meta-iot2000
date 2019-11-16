LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

FILESEXTRAPATHS_prepend := "${THISDIR}/configs:${THISDIR}/patches:"

LINUX_VERSION = "4.4.185-cip35"
SRC_URI = " \
    https://git.kernel.org/pub/scm/linux/kernel/git/cip/linux-cip.git/snapshot/linux-cip-${LINUX_VERSION}.tar.gz \
    file://defconfig \
    ${KERNEL_PATCHES}"
SRC_URI[sha256sum] = "fcdd46615fdc7e0e4ad3d73465d1489e3af72ed09efb8c748abec7be38586a5b"

KERNEL_PATCHES = " \
    file://0001-stmmac-pci-Make-stmmac_pci_info-structure-constant.patch \
    file://0002-stmmac-pci-Use-stmmac_pci_info-for-all-devices.patch \
    file://0003-stmmac-pci-Make-stmmac_pci_find_phy_addr-truly-gener.patch \
    file://0004-stmmac-pci-Select-quark_pci_dmi_data-from-quark_defa.patch \
    file://0005-stmmac-pci-Use-dmi_system_id-table-for-retrieving-PH.patch \
    file://0006-stmmac-pci-Adjust-IOT2000-matching.patch \
    file://0007-serial-8250_exar-Adjust-IOT2000-matching.patch \
    file://0008-mfd-intel_quark_i2c_gpio-Adjust-IOT2000-matching.patch \
    file://0009-gpio-sch-use-gpiochip-data-pointer.patch \
    file://0010-gpio-sch-Use-devm_gpiochip_add_data-for-gpio-registr.patch \
    file://0011-gpio-sch-Fix-Oops-on-module-load-on-Asus-Eee-PC-1201.patch \
    file://0012-gpio-sch-Implement-.get_direction.patch \
    file://0013-gpio-sch-Add-interrupt-support.patch \
    file://0014-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://0015-iot2000-hack-Adjust-pca9685-gpio-base-for-legacy-com.patch \
    file://0016-iot2000-hack-gpio-pca953x-provide-GPIO-base-based-on.patch \
    file://0017-iot2000-hack-gpio-pca953x-add-drive-property.patch \
    file://0018-iot2000-hack-pwm-pca-9685-Provide-chip-level-pwm_per.patch"

S = "${WORKDIR}/linux-cip-${LINUX_VERSION}"
