LICENSE = "MIT"

FILES_${PN} += "/data"

do_install_append () {
	install -d "${D}/data"
}
