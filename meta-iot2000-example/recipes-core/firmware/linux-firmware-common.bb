SUMMARY = "Collection of firmware files for popular wifi devices"
LICENSE = "MIT"

inherit packagegroup

RDEPENDS_${PN} = "\
	linux-firmware-iwlwifi-license linux-firmware-iwlwifi-135-6 \
	linux-firmware-iwlwifi-3160-7 linux-firmware-iwlwifi-3160-8 linux-firmware-iwlwifi-3160-9 \
	linux-firmware-iwlwifi-6000-4 linux-firmware-iwlwifi-6000g2a-5 linux-firmware-iwlwifi-6000g2a-6 \
	linux-firmware-iwlwifi-6000g2b-5 linux-firmware-iwlwifi-6000g2b-6 \
	linux-firmware-iwlwifi-6050-4 linux-firmware-iwlwifi-6050-5 \
	linux-firmware-iwlwifi-7260 \
	linux-firmware-iwlwifi-7265 \
	linux-firmware-iwlwifi-7265d linux-firmware-iwlwifi-8000c linux-firmware-iwlwifi-8265 \
	linux-firmware-broadcom-license linux-firmware-bcm4329 linux-firmware-bcm4330 linux-firmware-bcm4334 linux-firmware-bcm43340 linux-firmware-bcm4339 linux-firmware-bcm4354 \
	"
