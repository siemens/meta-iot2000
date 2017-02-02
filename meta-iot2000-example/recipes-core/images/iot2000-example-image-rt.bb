require iot2000-example-image.inc

# Skip processing of this recipe if linux-yocto-rt is not explicitly specified as the
# PREFERRED_PROVIDER for virtual/kernel. This avoids errors when trying
# to build multiple virtual/kernel providers.
python () {
    if d.getVar("PREFERRED_PROVIDER_virtual/kernel", True) != "linux-yocto-rt":
        raise bb.parse.SkipPackage("Set PREFERRED_PROVIDER_virtual/kernel to linux-yocto-rt to enable it")
}

DEPENDS = "linux-yocto-rt"

IMAGE_INSTALL_append = " rt-tests"
