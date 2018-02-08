FILESEXTRAPATHS_prepend := "${THISDIR}/swupdate:"

SRCREV = "012374087c747f05216a7f002e4b8a34bc142c52"

SRC_URI += "file://swupdate_handlers.lua"

DEPENDS += "efibootguard"

do_configure_prepend () {
        cp ${WORKDIR}/swupdate_handlers.lua ${S}
}
