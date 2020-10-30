WKS_FILE = "example-image.iot2000.swupdate.wks"

# needs to be in sync with wks setting
IMAGE_ROOTFS_SIZE = "2097152"
IMAGE_OVERHEAD_FACTOR = "1"
IMAGE_ROOTFS_EXTRA_SPACE = "0"

IMAGE_FSTYPES += "ext4.gz"

IMAGE_INSTALL += "swupdate"
IMAGE_INSTALL += "efibootguard-tools"
IMAGE_INSTALL += "persiststore"
