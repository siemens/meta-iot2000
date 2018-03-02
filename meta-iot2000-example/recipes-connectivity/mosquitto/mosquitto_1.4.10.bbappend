PV = "1.4.14"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI = "https://github.com/eclipse/mosquitto/archive/v${PV}.tar.gz \
           file://build.patch \
           file://mosquitto.service \
           file://docbook-path.patch \
"

DEPENDS += "xmlto-native docbook-xml-dtd4-native docbook-xsl-stylesheets-native"

SRC_URI[md5sum] = "3281625600824a948f7050f53c02ab03"
SRC_URI[sha256sum] = "6e880a77c395db63fe5a0a5530ad255e65464534290ab65211c072f812462bde"
