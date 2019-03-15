SUMMARY = "The next evolution IoT/IIoT OPC UA toolbox package for Node-RED based on node-opcua."

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
LICENSE = "Apache-2.0 & ISC & BSD & BSD-3-Clause & MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=fb4562eee6b20e9a23a17f38a9f2527a"

inherit npm-ng

NPM_LOCAL_INSTALL_DIR = "/home/root/.node-red"

do_install_append() {
    NODE_VERSION=$(npm --version | cut -d '.' -f 1)
    DEASYNC_BIN_DIR=${D}/${NPM_LOCAL_INSTALL_DIR}/node_modules/node-red-contrib-iiot-opcua/node_modules/deasync/bin
    rm -rf ${DEASYNC_BIN_DIR}/linux-ia32-node-[^$NODE_VERSION]*
    rm -rf ${DEASYNC_BIN_DIR}/linux-x*
    rm -rf ${DEASYNC_BIN_DIR}/darwin-*
    rm -rf ${DEASYNC_BIN_DIR}/win32-*
}

RDEPENDS_${PN} += "openssl-bin"

INSANE_SKIP_${PN} += "textrel"
