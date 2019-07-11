SUMMARY = "node red mindconnect node using mindconnect-nodejs library."

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "MIT & BSD-3-Clause & BSD-2-Clause & ISC & Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=f2855717eed783b240d92baadef2c81f"

inherit npm-ng

NPMPN = "@mindconnect/node-red-contrib-mindconnect"
NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

RDEPENDS_${PN} += "bash"
