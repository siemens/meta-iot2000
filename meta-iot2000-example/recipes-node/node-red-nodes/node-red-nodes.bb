SUMMARY = "Preinstalled Node-RED nodes for the IOT2000"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

NODE_RED_PACKAGES = " \
    node-red-dashboard \
    node-red-node-serialport \
    node-red-node-intel-gpio \
    node-red-contrib-boolean-logic \
    node-red-contrib-iiot-opcua \
    node-red-contrib-modbus \
    @mindconnect/node-red-contrib-mindconnect"

RDEPENDS_${PN} += " \
    node-red-dashboard \
    node-red-node-serialport \
    node-red-node-intel-gpio \
    node-red-contrib-boolean-logic \
    node-red-contrib-iiot-opcua \
    node-red-contrib-modbus \
    mindconnect-node-red-contrib-mindconnect"

python do_compile() {
    import json

    with open("package.json", 'w') as outfile:
        packages = d.getVar('NODE_RED_PACKAGES').split()
        json_objs = {
            'name': 'node-red-project',
            'description': 'A Node-RED Project',
            'version': '0.0.1',
            'private': True,
            'dependencies': { package: '*' for package in packages}
        }
        json.dump(json_objs, outfile, indent=2)
}

do_install() {
    install -d ${D}/home/root/.node-red/
    install -m 0644 ${S}/package.json ${D}/home/root/.node-red/
}

FILES_${PN} = "/home/root/.node-red/package.json"
