require recipes-devtools/nodejs/nodejs_6.inc
require recipes-devtools/nodejs/nodejs_lts.inc

INC_PR = "r1"

LIC_FILES_CHKSUM = "file://LICENSE;md5=14152103612601231d62308345463670"

SRC_URI += "file://0001-nodejs-add-compile-flag-options-for-quark.patch"

SRC_URI[src.md5sum] = "7fe69eb52c74fb2c8eb5f327d5b7e7b6"
SRC_URI[src.sha256sum] = "378b7b06ce6de96c59970908fc2a67278e1ece22be78030423297bf415c0a8c5"
