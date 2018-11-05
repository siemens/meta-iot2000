FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://main.conf \
    file://settings"

do_install_append() {
	sed -e 's/\(DESC="Connection Manager"\)/\0\n\nexport GNUTLS_NO_EXPLICIT_INIT=1/' \
	    -e 's/\(EXTRA_PARAM=\)""$/\1"--nodnsproxy"/' \
	    -i ${D}/etc/init.d/connman

	install -d ${D}/etc/connman
	install -m 0644 ${WORKDIR}/main.conf ${D}/etc/connman/main.conf

	install -d ${D}/var/lib/connman
	install -m 0600 ${WORKDIR}/settings ${D}/var/lib/connman/settings
}
