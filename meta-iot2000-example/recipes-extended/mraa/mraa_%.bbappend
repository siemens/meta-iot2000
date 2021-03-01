FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://0001-api-Add-explicit-close-methods-to-classes.patch \
    file://0002-led-Fix-and-cleanup-initialization.patch"

# Move mraa under /usr/lib/node, to be in the search path
do_install_append() {
    mv ${D}${libdir}/node_modules ${D}${libdir}/node
}

FILES_node-${PN} = "${prefix}/lib/node/"
