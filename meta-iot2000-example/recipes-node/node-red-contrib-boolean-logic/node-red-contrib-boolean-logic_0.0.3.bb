# Recipe created by recipetool

SUMMARY = "A set of Node-RED nodes for boolean logic"
# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d5a1ff81f6ad90b88ba24f2a1fd4db83"

SRC_URI = "npm://registry.npmjs.org;name=node-red-contrib-boolean-logic;version=${PV}"

NPM_SHRINKWRAP := "${THISDIR}/${PN}/npm-shrinkwrap.json"
NPM_LOCKDOWN := "${THISDIR}/${PN}/lockdown.json"

inherit npm

# Must be set after inherit npm since that itself sets S
S = "${WORKDIR}/npmpkg"
LICENSE_${PN} = "MIT"
