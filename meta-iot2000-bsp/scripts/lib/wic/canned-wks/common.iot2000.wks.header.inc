# short-description: Create an IOT2000 disk image
# long-description: Creates a partitioned EFI disk image for the SIMATIC IOT2000
# that the user can directly dd to boot media.

part --source efibootguard-efi --size 32 --extra-space 0 --overhead-factor 1 --ondisk mmcblk0 --label efi --part-type=EF00 --align 1024
part --source efibootguard-boot --size 32 --extra-space 0 --overhead-factor 1 --ondisk mmcblk0 --label boot0 --align 1024 --part-type=0700 --sourceparams "watchdog=60,revision=2,initrd=acpi-upgrades-iot2000.cpio"
