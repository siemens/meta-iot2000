require uclibc.inc
require uclibc-package.inc
require uclibc-git.inc

STAGINGCC = "gcc-cross-initial-${TARGET_ARCH}"
STAGINGCC_class-nativesdk = "gcc-crosssdk-initial-${TARGET_ARCH}"

DEPENDS = "virtual/${TARGET_PREFIX}binutils \
           virtual/${TARGET_PREFIX}gcc-initial \
           virtual/${TARGET_PREFIX}libc-initial \
           linux-libc-headers ncurses-native \
           libgcc-initial kern-tools-native"

RDEPENDS_${PN}-dev = "linux-libc-headers-dev"
