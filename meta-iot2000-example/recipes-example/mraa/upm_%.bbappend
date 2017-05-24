#The missing "meta-java" from Intel caused trouble so we use "java2" here
#Also we upgrade to version 1.0.1 to fit the mraa version

PV="1.0.1"

SRC_URI = "git://github.com/intel-iot-devkit/upm.git"
SRCREV="a2698fd560c9fa7917de33a65601bea50d218481"

PACKAGES := "${@oe_filter_out('${PN}-java', '${PACKAGES}', d)}"
PACKAGECONFIG = "nodejs python"
