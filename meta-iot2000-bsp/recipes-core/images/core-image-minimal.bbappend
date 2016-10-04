IMAGE_FSTYPES_append_iot2000 = " wic"

do_image_wic[depends] += "${PN}:do_bootimg"
