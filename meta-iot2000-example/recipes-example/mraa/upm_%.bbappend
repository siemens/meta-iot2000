#The missing "meta-java" from Intel caused trouble so we use "java2" here
#Also we upgrade to version 1.0.0 to fit the mraa version

PV="1.0.0"

SRC_URI = "git://github.com/intel-iot-devkit/upm.git"
SRCREV="13e2e7aeb8769707b91b62f23d6669d3ee1a8651"

RDEPENDS_${PN}-java = "java2-runtime mraa-java"