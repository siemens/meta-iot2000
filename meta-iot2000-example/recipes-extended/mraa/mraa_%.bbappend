# Move mraa under /usr/lib/node, to be in the search path

do_install:append() {
    mv ${D}${libdir}/node_modules ${D}${libdir}/node
}

FILES:node-${PN} = "${prefix}/lib/node/"
