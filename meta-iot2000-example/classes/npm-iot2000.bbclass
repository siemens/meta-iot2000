inherit npm

def node_pkgname(d):
    bpn = d.getVar('BPN')
    if bpn.startswith("node-") and not bpn.startswith("node-red"):
        return bpn[5:]
    return bpn

do_compile_prepend() {
    unused="${@bb.utils.export_proxies(d)}"
}

do_install_prepend() {
    unused="${@bb.utils.export_proxies(d)}"
}

do_install_append() {
    # undo what poky does - it does not work with our node-red
    mv ${D}${libdir}/node ${D}${libdir}/node_modules
}

NPM_INSTALLDIR = "${libdir}/node_modules/${NPMPN}"
