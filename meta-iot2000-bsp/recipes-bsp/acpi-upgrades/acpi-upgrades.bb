FILESEXTRAPATHS_prepend := "${THISDIR}/tables:"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${IOT2000_MIT_LICENSE};md5=838c366f69b72c5df05c96dff79b35f2"

inherit deploy

DEPENDS = "acpica-native"

SRC_URI_iot2000 = "file://iot2000"

do_compile() {
	rm -fr ${WORKDIR}/acpi-upgrades

	install -d ${WORKDIR}/acpi-upgrades/kernel/firmware/acpi

	for table in ${WORKDIR}/*/*.asl; do
		dest_table=$(basename $table)
		${STAGING_DIR_NATIVE}${bindir_native}/iasl \
			-p ${WORKDIR}/acpi-upgrades/kernel/firmware/acpi/$dest_table $table
	done

	cd ${WORKDIR}/acpi-upgrades
	find kernel | cpio -H newc -o > ${WORKDIR}/acpi-upgrades-${MACHINE}.cpio
}

do_deploy() {
	cp ${WORKDIR}/acpi-upgrades-${MACHINE}.cpio ${DEPLOYDIR}
}

addtask deploy before do_build after do_compile
