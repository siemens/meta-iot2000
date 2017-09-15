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


Native Build
------------

On a compatible distribution, install the
[packages](http://www.yoctoproject.org/docs/2.2/mega-manual/mega-manual.html#packages)
that Yocto 2.2 requires.

Furthermore, install the kas build tool:

```shell
$ pip3 install kas
```

Now you can build the example image like this:

```shell
$ kas build meta-iot2000-example/kas.yml
```

To build the BSP image instead, just specify the corresponding configuration
file instead:

```shell
$ kas build meta-iot2000-bsp/kas.yml
```

You can also reproduce the Windows or Linux SDK this way:

```shell
$ kas build meta-iot2000-example/sdk-kas-windows-i586.yml
$ kas build meta-iot2000-example/sdk-kas-linux-x86.yml
```

Docker Build
------------

Make sure Docker is installed and properly configured for your host system. You
may have to switch the storage driver away from legacy aufs, see
[Docker documentation](https://docs.docker.com/engine/userguide/storagedriver/selectadriver),
if kas warns about this.

Now run you can generate the desired image:

```shell
$ docker run -v $(pwd):/shared-volume:rw -e USER_ID=$(id -u) --rm -t -i \
             --storage-opt size=50G kasproject/kas:0.11.0 sh -c "
      cd /shared-volume &&
      git clone https://github.com/siemens/meta-iot2000 &&
      kas build meta-iot2000/meta-iot2000-example/kas.yml"
```

The above command disposes the build container after use, keeping downloads and
build results in the current work directory.

You may want to use the container interactively:

```shell
$ docker run -v $(pwd):/shared-volume:rw -e USER_ID=$(id -u) -t -i \
             --storage-opt size=50G kasproject/kas:0.11.0
# inside the container
$ cd /shared-volume
$ git clone https://github.com/siemens/meta-iot2000
$ kas build meta-iot2000/meta-iot2000-example/kas.yml
...
```

If you are building from within a proxy-restricted network, make sure the
settings are available via the standard environment variables and add

```
    -e http_proxy=$http_proxy -e https_proxy=$https_proxy \
    -e ftp_proxy=$ftp_proxy -e no_proxy=$no_proxy
```

to the Docker run command above.


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
