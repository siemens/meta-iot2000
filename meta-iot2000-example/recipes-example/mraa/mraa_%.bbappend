#This patch will include the SIMATIC IOT2000 as a known board that is similar to Galileo Gen 2
#Also the missing "meta-java" from Intel caused trouble so we use "java2" here

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " file://0001-Include-support-for-SIMATIC-IOT2000-platform.patch \
		   file://0002-intel_galileo_rev_g.c-use-pincmd-to-set-OUT_HIGH-ins.patch"

RDEPENDS_${PN}-java = "java2-runtime"