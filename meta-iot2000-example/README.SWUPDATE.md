# Example for efibootguard + SWUpdate support with meta-iot2000

The [kas](https://pypi.python.org/pypi/kas) recipes in

```
meta-iot2000/meta-iot2000-example/kas-update{,-rt}.yml
```

build the base image as well as an update artifact without and with a
real-time kernel respectively, ready to be fed to `SWUpdate`. The recipes contain all needed layer
references.

For `SWUpdate` integration, the official [meta-swupdate](https://github.com/sbabic/meta-swupdate)
layer is used. Per default it installs an init script to start up a webserver for update purposes,
which is not needed for manual updates. For this purpose, it is replaced by an empty
init script.

This example of `SWUpdate` and `efibootguard` integration provides manual update capability only.


The manual update process means, that the `swu` file must be copied onto the finished SD-card. To use it with swupdate, the following command is used:

```
swupdate -i <filepath>.swu
```

## Created artifacts

The aforementioned kas yml files produce the folllowing artifacts in the build folder:

* A flashable image: `tmp/deploy/images/iot2000/iot2000-example-image-iot2000.wic`
* An update artifact: `tmp/deploy/images/iot2000/iot2000-update-image-iot2000.swu`

*Note*:
Per default, the root filesystem included in the update artifact is identical to the one contained in the wic file. The simplest way to enhance the update artifact is to make it depend on a different image and set `SWUPDATE_IMAGES, SWUPDATE_IMAGES_FSTYPES, and IMAGE_DEPENDS` accordingly. See `meta-iot2000-example/recipes-core/images/iot2000-update-image.bb` for example.
