#This .bbappend file will set the mraa version to 1.5.1, where the SIMATIC 
#IOT2000 board name is already included.
#Also the missing "meta-java" from Intel caused trouble so we use "java2" here

PV="1.5.1"

SRC_URI = "git://github.com/intel-iot-devkit/mraa.git"
SRCREV="6f9b470d8d25e2c8ba1586cd9d707b870ab30010"

RDEPENDS_${PN}-java = "java2-runtime"
PROVIDES = "node-mraa"