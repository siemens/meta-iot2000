This README file contains information on building the meta-iot2000
BSP layer, and booting the images contained in the output directory.
Please see the corresponding sections below for details.


Dependencies
============

This layer depends on:

```
  URI: git://git.yoctoproject.org/poky
  layers: meta, meta-yocto, meta-yocto-bsp
  branch: morty

  URI: git://git.yoctoproject.org/meta-intel
  layers: meta-intel
  branch: morty
```


Building the meta-iot2000 BSP Layer
===================================

This uses Yocto 2.2 (Morty) with the 4.4 Linux kernel provided by Yocto and
the meta-intel layer. The build has successfully been tested on Debian 8,
OpenSuse 42.2 and Fedora 25 but other recent distros are expected to work as
well.

## Prepare:

For setting up your host pc see the following description:
[3. Setting Up to Use the Yocto Project](http://www.yoctoproject.org/docs/2.1/mega-manual/mega-manual.html#yp-resources)

```shell
$ git clone git://git.yoctoproject.org/poky.git poky -b morty
$ git clone git://git.yoctoproject.org/meta-intel poky/meta-intel -b morty
$ git clone http://git.openembedded.org/meta-openembedded poky/meta-openembedded -b morty
```

For using tested revisions, you have to checkout these versions:

```shell
$ git -C poky checkout 6a1f33cc40bf
$ git -C poky/meta-intel checkout 6add41510412
$ git -C poky/meta-openembedded checkout fe5c83312de1
```

You may update to a newer Yocto versions as needed (e.g. to include security
fixes), but be aware of potential breakages. Tests were performed only against
the specified revisions so far.

## Download meta-iot2000 (unless already done):
```shell
$ git clone git://github.com/siemens/meta-iot2000 poky/meta-iot2000
```

## Enter Build Environment:

```shell
$ source poky/oe-init-build-env iot2000-build
```

## Configure:

```diff
--- iot2000-build/conf/bblayers.conf.old
+++ iot2000-build/conf/bblayers.conf
@@ -9,4 +9,7 @@
   /home/build/poky/meta \
   /home/build/poky/meta-poky \
   /home/build/poky/meta-yocto-bsp \
+  /home/build/poky/meta-openembedded/meta-oe \
+  /home/build/poky/meta-intel \
+  /home/build/poky/meta-iot2000/meta-iot2000-bsp \
   "
```

```diff
--- iot2000-build/conf/local.conf.old
+++ iot2000-build/conf/local.conf
@@ -34,7 +34,7 @@
 #MACHINE ?= "edgerouter"
 #
 # This sets the default machine to be qemux86 if no other machine is selected:
-MACHINE ??= "qemux86"
+MACHINE ??= "iot2000"
 
 #
 # Where to place downloads
```

## Create Minimal Image:

```shell
$ bitbake core-image-minimal
```


Booting the Image from SD card
==============================

Under Linux, insert an unused SD card. Assuming the SD card takes device
/dev/mmcblk0, use dd to copy the image to it. For example:

```shell
$ sudo dd if=tmp/deploy/images/iot2000/core-image-minimal-iot2000.wic of=/dev/mmcblk0 bs=4M oflag=sync
```

If you want to ssh into the system, you can use the root terminal to
ifconfig the IP address and use that to ssh in. The root password is
empty, so to log in type 'root' for the user name and hit 'Enter' at
the Password prompt and you should be in.


Booting the Image from USB stick
================================

Under Linux, insert an unused USB stick. Assuming the USB stick takes device
/dev/sda, use dd to copy the image to it. For example:

```shell
$ sudo dd if=tmp/deploy/images/iot2000/core-image-minimal-iot2000.wic of=/dev/sda bs=4M oflag=sync
```

In addition, you have to change the boot config. On the first partition,
navigate to the folder loader/entries, open the file boot.conf and change the
following:

```diff
--- loader/entries/boot.conf.old
+++ loader/entries/boot.conf
title boot
linux /bzImage
-options LABEL=Boot root=/dev/mmcblk0p2 console=ttyS1,115200n8 reboot=efi,warm rw LABEL=boot debugshell=5 rootwait
+options LABEL=Boot root=/dev/sda2 console=ttyS1,115200n8 reboot=efi,warm rw LABEL=boot debugshell=5 rootwait
```
