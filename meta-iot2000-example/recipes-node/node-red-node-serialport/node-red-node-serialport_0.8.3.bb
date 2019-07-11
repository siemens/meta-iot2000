SUMMARY = "Node-RED nodes to talk to serial ports"

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "MIT & ISC & Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=6621dba0ae00c5595cc3b482008b021a"

inherit npm-ng

NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

INSANE_SKIP_${PN} += "textrel"
