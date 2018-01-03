require recipes-devtools/nodejs/nodejs_6.inc
require recipes-devtools/nodejs/nodejs_lts.inc

INC_PR = "r1"

LIC_FILES_CHKSUM = "file://LICENSE;md5=14152103612601231d62308345463670"

SRC_URI += "file://0001-nodejs-add-compile-flag-options-for-quark.patch"

SRC_URI[src.md5sum] = "82970532171602d1caa2b7c5bb5828fe"
SRC_URI[src.sha256sum] = "088788d1c887309f8650730908dbf6f09140077a8aaf582021af4bef2a6d6b84"
