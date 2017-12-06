IMAGE_FSTYPES_append_iot2000 = " wic"

WKS_FILE = "wic-image.${MACHINE}.wks"

WKS_FILE_DEPENDS_BOOTLOADERS_x86 = "systemd-boot"

require recipes-core/images/acpi-upgrades.inc
