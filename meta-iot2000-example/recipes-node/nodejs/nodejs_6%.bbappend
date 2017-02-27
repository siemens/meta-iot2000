#This recipe adds a patch to nodejs v6.9.2 to add a compiler flag option for quark

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " file://0001-nodejs-add-compile-flag-options-for-quark.patch"