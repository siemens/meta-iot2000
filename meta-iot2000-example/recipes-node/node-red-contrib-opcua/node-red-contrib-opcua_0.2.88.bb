SUMMARY = "A Node-RED nodes to communicate or serve via OPC UA."

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "BSD-2-Clause & BSD-3-Clause & Apache-2.0 & ISC & MIT | GPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ba714a6d98076972d6313481e4887def"

inherit npm-ng

NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

INSANE_SKIP:${PN} += "textrel"
