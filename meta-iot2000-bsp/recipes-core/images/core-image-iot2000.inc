require wic-image.inc

DEPENDS += "acpi-upgrades"
do_bootimg[depends] += "acpi-upgrades:do_deploy"

IMAGE_INSTALL_append = " switchmode"

DEPENDS += "gptfdisk-native efibootguard-native"
