require recipes-core/images/core-image-minimal.bb
require recipes-core/images/core-image-iot2000.inc
require iot2000-example-image.inc

DEPENDS += "gptfdisk-native"
