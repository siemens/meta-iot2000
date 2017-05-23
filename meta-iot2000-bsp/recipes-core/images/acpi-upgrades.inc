# Workaround for missing initrd support in wic plugin bootimg-efi before 2.3

do_copy_to_initrd() {
	install -d ${HDDDIR}/EFI/BOOT
	install ${DEPLOY_DIR_IMAGE}/acpi-upgrades-${MACHINE}.cpio ${HDDDIR}/EFI/BOOT/
}

addtask copy_to_initrd after do_bootimg before do_image_wic
