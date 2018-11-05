FILESEXTRAPATHS_prepend := "${COREBASE}/meta/recipes-connectivity/ofono/ofono:"

require recipes-connectivity/ofono/ofono.inc

SRC_URI  = "\
  ${KERNELORG_MIRROR}/linux/network/${BPN}/${BP}.tar.xz \
  file://ofono \
"
SRC_URI[md5sum] = "997b2c6ac56fd54b6b797435f0bbca51"
SRC_URI[sha256sum] = "92e18c20c889addda648aefbb5e3ab1238007d88b18449f407a96533afe18026"

# something is fishy with the 1.26 parallel build...
PARALLEL_MAKE = ""
