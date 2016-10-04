SUMMARY = "Sets up ACM gadget device via configfs"
SECTION = "base"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${IOT2000_GPLv2_LICENSE};md5=751419260aa954499f7abaabaa882bbe"

inherit update-rc.d

INITSCRIPT_PACKAGES = "${PN}"
INITSCRIPT_NAME = "${PN}"

SRC_URI = " \
    file://acm-gadget \
    "

do_install () {
        install -d ${D}${sysconfdir}/init.d
        cat ${WORKDIR}/acm-gadget | \
          sed -e 's,/etc,${sysconfdir},g' \
              -e 's,/usr/sbin,${sbindir},g' \
              -e 's,/var,${localstatedir},g' \
              -e 's,/usr/bin,${bindir},g' \
              -e 's,/usr,${prefix},g' > ${D}${sysconfdir}/init.d/acm-gadget
        chmod a+x ${D}${sysconfdir}/init.d/acm-gadget
}
