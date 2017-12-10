inherit npm

do_install() {
	mkdir -p ${NPM_INSTALLDIR}/
	cp -a ${S}/* ${NPM_INSTALLDIR}/ --no-preserve=ownership
}
