IMAGE_FSTYPES += "ext4.gz"

require recipes-core/images/core-image-minimal.bb
require recipes-core/images/core-image-iot2000.inc
require iot2000-example-image.inc

IMAGE_INSTALL_append += "swupdate efibootguard-tools"

DEPENDS += "gptfdisk-native efibootguard-native"
