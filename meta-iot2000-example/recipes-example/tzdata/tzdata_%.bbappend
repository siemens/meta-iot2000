do_install_append () {
        cp -pP "${S}/zone1970.tab" ${D}${datadir}/zoneinfo
}

FILES_${PN} += "${datadir}/zoneinfo/zone1970.tab"
