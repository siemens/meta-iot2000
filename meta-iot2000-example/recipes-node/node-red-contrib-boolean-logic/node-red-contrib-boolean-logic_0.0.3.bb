# Recipe created by recipetool

SUMMARY = "A set of Node-RED nodes for boolean logic"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d5a1ff81f6ad90b88ba24f2a1fd4db83"

SRC_URI = "npm://registry.npmjs.org;name=node-red-contrib-boolean-logic;version=${PV}"

NPM_SHRINKWRAP := "${THISDIR}/${PN}/npm-shrinkwrap.json"
NPM_LOCKDOWN := "${THISDIR}/${PN}/lockdown.json"

inherit npm-iot2000

# Must be set after inherit npm since that itself sets S
S = "${WORKDIR}/npmpkg"
LICENSE_${PN} = "MIT"
