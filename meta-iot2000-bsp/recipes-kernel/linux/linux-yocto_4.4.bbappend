FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://0001-stmmac-adding-support-for-platform-IOT2000.patch \
    file://0002-serial-uapi-Add-support-for-bus-termination.patch \
    file://0003-serial-8250_pci-Use-symbolic-constants-for-EXAR-s-MP.patch \
    file://0004-serial-8250_pci-Fix-EXAR-feature-control-register-co.patch \
    file://0005-serial-8250_pci-Add-support-for-IOT2000-platform.patch \
    file://0006-x86-efi-Add-capsule-update-driver-for-Intel-Quark.patch \
    file://0007-serial-8250_pci-Add-support-for-accessing-red-LED-vi.patch \
    file://iot2000.cfg"

LINUX_VERSION_iot2000 = "${LINUX_VERSION_INTEL_COMMON}"
COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
KBRANCH_iot2000 = "${KBRANCH_INTEL_COMMON}"
SRCREV_meta_iot2000 ?= "${SRCREV_META_INTEL_COMMON}"
SRCREV_machine_iot2000 ?= "${SRCREV_MACHINE_INTEL_COMMON}"
KERNEL_FEATURES_append_iot2000 = ""
