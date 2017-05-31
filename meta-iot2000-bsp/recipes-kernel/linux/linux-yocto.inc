FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += " \
    file://0001-stmmac-Add-support-for-SIMATIC-IOT2000-platform.patch \
    file://0002-serial-uapi-Add-support-for-bus-termination.patch \
    file://0003-serial-8250_pci-Use-symbolic-constants-for-EXAR-s-MP.patch \
    file://0004-serial-8250_pci-Fix-EXAR-feature-control-register-co.patch \
    file://0005-serial-8250_pci-Add-support-for-IOT2000-platform.patch \
    file://0006-serial-8250_pci-Add-support-for-red-user-LED-on-IOT2.patch \
    file://0007-spi-pxa2xx-Factor-out-handle_bad_msg.patch \
    file://0008-spi-pxa2xx-Prepare-for-edge-triggered-interrupts.patch \
    file://0009-spi-pca2xx-pci-Allow-MSI.patch \
    file://0010-efi-Move-efi_status_to_err-to-drivers-firmware-efi.patch \
    file://0011-efi-Add-capsule-update-support.patch \
    file://0012-x86-efi-Force-EFI-reboot-to-process-pending-capsules.patch \
    file://0013-efi-Add-misc-char-driver-interface-to-update-EFI-fir.patch \
    file://0014-efi-capsule-Make-efi_capsule_pending-lockless.patch \
    file://0015-efi-capsule-Move-capsule-to-the-stack-in-efi_capsule.patch \
    file://0016-efi-capsule-Allocate-whole-capsule-into-virtual-memo.patch \
    file://0017-efi-capsule-Fix-return-code-on-failing-kmap-vmap.patch \
    file://0018-efi-capsule-Remove-pr_debug-on-ENOMEM-or-EFAULT.patch \
    file://0019-efi-capsule-Clean-up-pr_err-info-messages.patch \
    file://0020-efi-capsule-Adjust-return-type-of-efi_capsule_setup_.patch \
    file://0021-efi-capsule-loader-Use-a-cached-copy-of-the-capsule-.patch \
    file://0022-efi-capsule-loader-Redirect-calls-to-efi_capsule_set.patch \
    file://0023-efi-capsule-loader-Use-page-addresses-rather-than-st.patch \
    file://0024-efi-capsule-Add-support-for-Quark-security-header.patch \
    file://0025-mfd-intel_quark_i2c_gpio-Use-dmi_system_id-table-for.patch \
    file://0026-mfd-intel_quark_i2c_gpio-Add-support-for-SIMATIC-IOT.patch \
    file://0027-iot2000-hack-Work-around-DSDT-mistake.patch \
    file://iot2000.scc"

LINUX_VERSION_iot2000 = "${LINUX_VERSION_INTEL_COMMON}"
COMPATIBLE_MACHINE_iot2000 = "iot2000"
KMACHINE_iot2000 = "intel-quark"
KBRANCH_iot2000 = "${KBRANCH_INTEL_COMMON}"
SRCREV_meta_iot2000 ?= "${SRCREV_META_INTEL_COMMON}"
SRCREV_machine_iot2000 ?= "${SRCREV_MACHINE_INTEL_COMMON}"
KERNEL_FEATURES_append_iot2000 = ""
