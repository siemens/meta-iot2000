# short-description: Create an IOT2000 disk image
# long-description: Creates a partitioned EFI disk image for the SIMATIC IOT2000
# that the user can directly dd to boot media.

part /boot --source bootimg-efi --sourceparams="loader=systemd-boot,initrd=acpi-upgrades-iot2000.cpio" --ondisk mmcblk0 --label msdos --active --align 1024
