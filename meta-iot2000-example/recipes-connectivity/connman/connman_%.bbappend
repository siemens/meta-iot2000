FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://main.conf"

do_install_append() {
	sed -i 's/\(DESC="Connection Manager"\)/\0\n\nexport GNUTLS_NO_EXPLICIT_INIT=1/' \
		${D}/etc/init.d/connman

	install -d ${D}/etc/connman
	install -m 0644 ${WORKDIR}/main.conf ${D}/etc/connman/main.conf
}
