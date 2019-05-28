SUMMARY = "The all in one Modbus TCP and Serial contribution package for Node-RED"

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=38c55ac37ed977af78e113caffd06846"

inherit npm-ng

NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

INSANE_SKIP_${PN} += "textrel"
