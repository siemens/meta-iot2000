LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=d7810fab7487fb0aad327b76f1be7cd7"

SRC_URI = " \
    git://git.kernel.org/pub/scm/linux/kernel/git/bwh/linux-cip;protocol=https"
SRCREV = "31e672f83ef8d2bd2e390a94a2b5904c17d053f6"
LINUX_VERSION = "4.4.138-cip25"

KERNEL_PATCHES = " \
    file://0001-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://0002-iot2000-hack-Adjust-pca9685-gpio-base-for-legacy-com.patch \
    file://0003-iot2000-hack-gpio-pca953x-provide-GPIO-base-based-on.patch \
    file://0004-iot2000-hack-gpio-pca953x-add-drive-property.patch \
    file://0005-iot2000-hack-pwm-pca-9685-Provide-chip-level-pwm_per.patch"

S = "${WORKDIR}/git"
