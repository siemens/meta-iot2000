DESCRIPTION = "Linux Kernel for IOT2000 based on CIP SLTS version"
SECTION = "kernel"

require recipes-kernel/linux/linux-yocto.inc
require linux-cip_4.4.inc

PV = "${LINUX_VERSION}"

LINUX_VERSION_EXTENSION = ""

COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"

# Accelerated entropy collection.
# These are not yet ready for the -rt kernel.
KERNEL_PATCHES += " \
    file://0019-random-replace-non-blocking-pool-with-a-Chacha20-bas.patch \
    file://0020-random-make-dev-urandom-scalable-for-silly-userspace.patch \
    file://0021-random-add-backtracking-protection-to-the-CRNG.patch \
    file://0022-random-remove-stale-maybe_reseed_primary_crng.patch \
    file://0023-random-use-chacha20-for-get_random_int-long.patch \
    file://0024-random-convert-get_random_int-long-into-get_random_u.patch \
    file://0025-random-invalidate-batched-entropy-after-crng-init.patch \
    file://0026-random-silence-compiler-warnings-and-fix-race.patch \
    file://0027-random-add-wait_for_random_bytes-API.patch \
    file://0028-random-fix-crng_ready-test.patch \
    file://0029-random-use-a-different-mixing-algorithm-for-add_devi.patch \
    file://0030-random-only-read-from-dev-random-after-its-pool-has-.patch \
    file://0031-random-fix-soft-lockup-when-trying-to-read-from-an-u.patch \
    file://0032-random-try-to-actively-add-entropy-rather-than-passi.patch"
