SUMMARY = "The all in one Modbus TCP and Serial contribution package for Node-RED"

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "BSD-2-Clause & BSD-3-Clause & Apache-2.0 & ISC & MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=4ce3d0350364f3efff545d6ba54f61eb"

inherit npm-ng

export PYTHON = "python3"

NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

INSANE_SKIP:${PN} += "textrel"
