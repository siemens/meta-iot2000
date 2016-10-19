require  recipes-core/images/core-image-minimal.bb

DESCRIPTION = "Example image for the IOT2000 platform"

IMAGE_FSTYPES_append_iot2000 = " wic"

do_image_wic[depends] += "${PN}:do_bootimg"

WKS_FILE = "core-image-minimal.${MACHINE}.wks"

#example features
IMAGE_FEATURES += " package-management"
IMAGE_FEATURES += " dev-pkgs"
IMAGE_FEATURES += " eclipse-debug"
IMAGE_FEATURES += " tools-sdk"
IMAGE_INSTALL_append = " switchmode"
IMAGE_INSTALL_append = " opkg"
IMAGE_INSTALL_append = " imageversionfile"
IMAGE_INSTALL_append = " dmidecode"
IMAGE_INSTALL_append = " openssh"
IMAGE_INSTALL_append = " screen minicom"
IMAGE_INSTALL_append = " mraa upm"
IMAGE_INSTALL_append = " parted e2fsprogs dosfstools"
IMAGE_INSTALL_append = " nodejs nodejs-npm"
IMAGE_INSTALL_append = " curl"
IMAGE_INSTALL_append = " pciutils"
IMAGE_INSTALL_append = " iptables"
IMAGE_INSTALL_append = " cmake"
IMAGE_INSTALL_append = " nano"
IMAGE_INSTALL_append = " iw wpa-supplicant"
IMAGE_INSTALL_append = " galileo-target"
