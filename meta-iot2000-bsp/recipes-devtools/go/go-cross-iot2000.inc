FILESEXTRAPATHS_prepend := "${THISDIR}/common:"

SRC_URI += " \
    file://0001-runtime-Implement-i386-atomic-quadword-ops-alternati.patch \
    file://0002-Revert-runtime-check-and-fail-early-with-a-message-i.patch \
    file://0003-cmd-internal-obj-x86-cmd-compile-internal-x86-Add-In.patch \
    file://go-wrapper \
    "

do_install_append() {
    mv ${D}${bindir}/go ${D}${bindir}/go.bin
    install -m755 ${WORKDIR}/go-wrapper ${D}${bindir}/go
}
