#
# Common configuration for all MACHINES of the intel-quark type
#

DEFAULTTUNE ?= "i586-nlp-32"
require conf/machine/include/tune-i586-nlp.inc
require conf/machine/include/x86-base.inc

# gnutls padlock code uses CMOV instruction in assembly which
# is not valid for Quark.
EXTRA_OECONF:append:pn-gnutls_intel-quark = " --disable-padlock"
EXTRA_OECONF:append:pn-openssl_intel-quark = " no-asm" 
