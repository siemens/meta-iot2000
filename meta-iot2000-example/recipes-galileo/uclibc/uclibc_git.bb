require uclibc.inc
require uclibc-package.inc
require uclibc-git.inc

STAGINGCC = "gcc-cross-initial-${TARGET_ARCH}"
STAGINGCC_class-nativesdk = "gcc-crosssdk-initial-${TARGET_ARCH}"

DEPENDS = "virtual/${TARGET_PREFIX}binutils \
           virtual/${TARGET_PREFIX}gcc \
           virtual/${TARGET_PREFIX}compilerlibs \
           linux-libc-headers ncurses-native \
           kern-tools-native"

RDEPENDS_${PN}-dev = "linux-libc-headers-dev"
