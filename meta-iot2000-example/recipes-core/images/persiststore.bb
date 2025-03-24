LICENSE = "MIT"

FILES:${PN} += "/data"

do_install:append () {
	install -d "${D}/data"
}
