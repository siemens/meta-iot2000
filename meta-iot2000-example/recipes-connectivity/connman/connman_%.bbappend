do_install_append() {
	sed -i 's/\(DESC="Connection Manager"\)/\0\n\nexport GNUTLS_NO_EXPLICIT_INIT=1/' \
		${D}/etc/init.d/connman
}
