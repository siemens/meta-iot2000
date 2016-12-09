#This .bbappend file will set the mraa version to 1.5.1, where the SIMATIC 
#IOT2000 board name is already included.
#Also the missing "meta-java" from Intel caused trouble so we use "java2" here

PV="1.5.1"

SRC_URI = "git://github.com/intel-iot-devkit/mraa.git"
SRCREV="6f9b470d8d25e2c8ba1586cd9d707b870ab30010"

RDEPENDS_${PN}-java = "java2-runtime"

#include node-mraa so the lib can be used by node-red
PROVIDES = "node-mraa"

#The mraa project has some trouble installing the module in the right place, so here is an workaround.
#PYTHON_SITEPACKAGES_DIR contains "dist-packages", I really don't know why...

FILES_python-${PN} = "${PYTHON_SITEPACKAGES_DIR}/../site-packages"
do_install_append(){
	install -d ${D}/usr/lib/python2.7/site-packages/
	cp ${D}/usr/lib/python2.7/dist-packages/* ${D}/usr/lib/python2.7/site-packages
}
