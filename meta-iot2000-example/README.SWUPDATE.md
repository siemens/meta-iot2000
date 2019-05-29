# Example for efibootguard + SWUpdate support with meta-iot2000

[SWUpdate](https://github.com/sbabic/swupdate) is a software that supports
firmware and/or software updates targeting embedded devices.

It can be run as a stand-alone server in foreground or as a daemon listening
for connections via ethernet or IPC. Different backends can be configured to
support other 3rd party software to provide the update artifacts. These are
then pulled by SWUpdate to update the system.
The new boot loader EFI Boot Guard will take care that unsuccessful firmware
updates will be rolled back so that the system is not bricked.

To build the image, the kas tool is utilized.

The [kas](https://pypi.python.org/pypi/kas) recipes in

```
meta-iot2000/meta-iot2000-example/kas-update.yml
```

build the base image as well as an update artifact without and with a
real-time kernel respectively, ready to be fed to `SWUpdate`. The recipes
contain all needed layer references.

For SWUpdate integration, the official
[meta-swupdate](https://github.com/sbabic/meta-swupdate) layer is used. Per
default it installs an init script to start up a webserver for update purposes,
which is not needed for manual updates. For this purpose, it is replaced by an
empty init script.

This example of `SWUpdate` and `efibootguard` integration provides manual
update capability only.


The manual update process means, that the `swu` file must be copied onto the
finished SD-card before booting or via, e.g., SSH to the booted device.

To use it with swupdate, the following command is used:

```
swupdate -i <filepath>.swu
```

Then a reboot of the system into the newly installed image is required. After
this version came up successfully, the installation has to be confirmed:

```
bg_setenv -c
```

Without this, the next reboot will fall back to the previous image version.

*NOTE*: The setup can be adapted to work with backends like, e.g., hawkBit.

## Created artifacts

The aforementioned kas yml files produce the following artifacts in
`<build_folder>/tmp/deploy/images/`:

* A flashable image: `iot2000-example-image-swu-iot2000.wic`
* An update artifact: `iot2000-example-image-iot2000.swu`

*Note*:
Per default, the root filesystem included in the update artifact is identical to
the one contained in the wic file. The simplest way to change this is to make it
depend on a different image and set `SWUPDATE_IMAGES, SWUPDATE_IMAGES_FSTYPES,
and IMAGE_DEPENDS` accordingly. See
`meta-iot2000-example/recipes-core/images/iot2000-update-image.bb` for example.

The provided example configuration of swupdate registers a 'progress_firmware'
program as a hook to reboot the system automatically after swupdate installed
the artifact. This is done in `/etc/swupdate.cfg`.
