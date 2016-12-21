do_install() {
	install -d  ${D}/lib/firmware/
	install -d  ${D}/lib/firmware/brcm/
	install -d  ${D}/lib/firmware/rtlwifi/
	cp -r ./brcm/* ${D}/lib/firmware/brcm/
	cp -r ./rtlwifi/* ${D}/lib/firmware/rtlwifi/
}