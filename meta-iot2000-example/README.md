This README file contains information on building the meta-iot2000-example.

Dependencies
============

This layer depends on:

```
  URI: git://git.yoctoproject.org/poky
  layers: meta, meta-yocto, meta-yocto-bsp
  branch: krogoth

  URI: git://git.openembedded.org/meta-openembedded
  layers: meta-oe
  branch: krogoth

  URI: git://git.yoctoproject.org/meta-intel
  layers: meta-intel
  branch: krogoth

  URI: git://git.yoctoproject.org/meta-java
  layers: meta-java
  branch: master

  URI: git://git.yoctoproject.org/meta-intel-iot-middleware
  layers: meta-intel-iot-middleware
  branch: master

  URI: git://github.com/siemens/meta-iot2000
  layers: meta-iot2000-bsp
  branch: master
```


Building the meta-iot2000 Example Image Layer
=============================================

This layer builds upon the meta-iot2000-bsp layer and shares its [dependencies
and setup procedures](../meta-iot2000-bsp/README.md). Listed below are the
additional / differing steps.

## Prepare:

Run additional commands to clone and checkout further dependencies.

```shell
$ git clone git://git.openembedded.org/meta-openembedded poky/meta-oe -b krogoth
$ git clone git://git.yoctoproject.org/meta-java poky/meta-java
$ git clone git://git.yoctoproject.org/meta-intel-iot-middleware poky/meta-intel-iot-middleware -b master
```

```shell
$ git -C poky/meta-oe checkout 247b1267bbe9
$ git -C poky/meta-java checkout 9edf7d5aa5bd
$ git -C poky/meta-intel-iot-middleware checkout 821cf14c8304
```

Then download meta-iot2000 (if not done already) and enter the build
environment.

## Configure:

```diff
--- conf/bblayers.conf.old
+++ conf/bblayers.conf
@@ -9,4 +9,10 @@
   /home/build/poky/meta \
   /home/build/poky/meta-poky \
   /home/build/poky/meta-yocto-bsp \
+  /home/build/poky/meta-oe/meta-oe \
+  /home/build/poky/meta-intel \
+  /home/build/poky/meta-java \
+  /home/build/poky/meta-intel-iot-middleware \
+  /home/build/poky/meta-iot2000/meta-iot2000-bsp \
+  /home/build/poky/meta-iot2000/meta-iot2000-example \
   "
```

This replaces the changes to conf/bblayers.conf documented in
()[../meta-iot2000-bsp/README.md]. The changes to conf/local.conf are the same.

## Create Example Image:

```shell
$ bitbake iot2000-example-image

```


Booting the Image
=================

Under Linux, insert an unused SD card. Assuming the SD card takes device
/dev/mmcblk0, use dd to copy the image to it. For example:

```shell
$ sudo dd if=tmp/deploy/images/iot2000/iot2000-example-image-iot2000.wic of=/dev/mmcblk0 bs=4M oflag=sync
```

The image starts with a preconfigured IP 192.168.200.1 on the first Ethernet
interface. You can use ssh to connect to the system.

NOTE: The root password is empty and should be changed before connecting the
system to an untrustworthy network.
