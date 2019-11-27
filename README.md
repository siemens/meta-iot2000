IOT2000 Board Support Package
=============================

This packages contains the following elements:

- meta-iot2000-bsp
- meta-iot2000-example

For updates, please visit https://github.com/siemens/meta-iot2000. We are
also accepting issue reports, feature suggestions and patches this way.


meta-iot2000-bsp
----------------

Use this Yocto layer to enable all hardware features of the IOT2000 device. It
allows to build standard Yocto images which will contain the required kernel,
configurations and tools and will emit a bootable SD card image.


meta-iot2000-example
--------------------

This Yocto layer builds on top of meta-iot2000-bsp, providing an exemplary image
with additional tools and services to exploit features of the IOT2000
conveniently.

This layer shall only be considered as a starting point for own developments. It
is not configured to provide product-grade maturity and security.


Building an Image
=================

There are two recommended ways to build one of the provided images, may they
be original or already customized: natively on a Linux machine or inside a
Docker container.

**Note:** Before starting the build, make sure that your working directory is
located on a native Linux file system such as ext4, xfs, btrfs, etc. NTFS is
known to **not** work.


Native Build
------------

On a compatible distribution, install the
[packages](https://www.yoctoproject.org/docs/2.6/mega-manual/mega-manual.html#required-packages-for-the-build-host)
that Yocto 2.6 requires.

Furthermore, install the kas build tool:

```shell
$ sudo pip3 install kas
```

Clone the meta-iot2000 repository (or unpack an archive of it) into a work
directory:

```shell
$ git clone https://github.com/siemens/meta-iot2000
```

Now you can build the example image like this:

```shell
$ kas build meta-iot2000/kas-example.yml
```

To build the BSP image instead, just specify the corresponding configuration
file instead:

```shell
$ kas build meta-iot2000/kas-bsp.yml
```

You can also reproduce the Windows or Linux SDK this way:

```shell
$ kas build meta-iot2000/kas-sdk-windows-i586.yml
$ kas build meta-iot2000/kas-sdk-linux-x64.yml
```


Docker Build
------------

Make sure Docker is installed and properly configured for your host system. You
may have to switch the storage driver away from legacy aufs, see
[Docker documentation](https://docs.docker.com/engine/userguide/storagedriver/selectadriver),
if kas warns about this.

Again, the first step is cloning of the repository (or unpacking an archive):

```shell
$ git clone https://github.com/siemens/meta-iot2000
```

Next, install the `kas-docker` script like this:

```shell
$ wget https://raw.githubusercontent.com/siemens/kas/2.0/kas-docker
$ chmod a+x kas-docker
```

Now you can generate a desired image. The following assumes that your user has
permission to use docker. Usually, this is achieved by adding the user to the
docker group (which has security implications). Note that running the build as
root does not work.

```shell
$ ./kas-docker build meta-iot2000/kas-example.yml
```

The above command disposes the build container after use, keeping downloads and
build results in the current work directory.

You may want to use the container interactively:

```shell
$ ./kas-docker shell meta-iot2000/kas-example.yml
```

If you are building from within a proxy-restricted network, make sure the
settings are available via the standard environment variables
(`http_proxy` etc.).


Booting the Image from SD card
==============================

Under Linux, insert an unused SD card. Assuming the SD card takes device
/dev/mmcblk0, use dd to copy the image to it. For example:

```shell
$ sudo dd if=build/tmp/deploy/images/iot2000/iot2000-example-image-iot2000.wic \
          of=/dev/mmcblk0 bs=4M oflag=sync
```

If you built the image in Docker, the .wic file will be located directly in the
meta-iot2000 directory.

The example image starts with the IP 192.168.200.1 preconfigured on the first
Ethernet interface. You can use ssh to connect to the system.

The BSP image does not configure the network. If you want to ssh into the
system, you can use the root terminal via UART to ifconfig the IP address and
use that to ssh in.

NOTE: The root password is empty and must be changed before connecting the
system to an untrustworthy network.


Booting the Image from USB stick
================================

Under Linux, insert an unused USB stick. Assuming the USB stick takes device
/dev/sda, use dd to copy the image to it. For example:

```shell
$ sudo dd if=build/tmp/deploy/images/iot2000/iot2000-example-image-iot2000.wic \
          of=/dev/sda bs=4M oflag=sync
```

In addition, you have to change the boot config. On the first partition,
navigate to the folder loader/entries, open the file boot.conf and change the
following:

```diff
--- loader/entries/boot.conf.orig
+++ loader/entries/boot.conf
@@ -1,3 +1,3 @@
 title boot
 linux /bzImage
-options LABEL=Boot root=/dev/mmcblk0p2 console=ttyS1,115200n8 reboot=efi,warm rw debugshell=5 rootwait initrd=EFI/BOOT/acpi-upgrades-iot2000.cpio
+options LABEL=Boot root=/dev/sda2 console=ttyS1,115200n8 reboot=efi,warm rw debugshell=5 rootwait initrd=EFI/BOOT/acpi-upgrades-iot2000.cpio
```
