FILESEXTRAPATHS_prepend := "${THISDIR}/nodejs:"

SRC_URI += " \
    file://0001-Restore-x87-port.patch \
    file://0002-Switch-to-x87-mode-when-targeting-ia32.patch \
    file://0003-Relax-check-in-ComputeInputFrameSize.patch"
