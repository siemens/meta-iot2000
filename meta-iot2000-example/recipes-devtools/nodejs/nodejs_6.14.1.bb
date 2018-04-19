require recipes-devtools/nodejs/nodejs_6.inc
require recipes-devtools/nodejs/nodejs_lts.inc

INC_PR = "r1"

LIC_FILES_CHKSUM = "file://LICENSE;md5=14152103612601231d62308345463670"

SRC_URI += "file://0001-nodejs-add-compile-flag-options-for-quark.patch"

SRC_URI[src.md5sum] = "7fd2a56d06e064bcc59446c1929f4ef5"
SRC_URI[src.sha256sum] = "82ca9917819db13c3a3484bd2bee1c58cd718aec3e4ad46026f968557a6717be"
