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

For further details, see [BSP readme](meta-iot2000-bsp/README.md).


meta-iot2000-example
--------------------

This Yocto layer builds on top of meta-iot2000-bsp, providing an exemplary image
with additional tools and services to exploit features of the IOT2000
conveniently.

This layer shall only be considered as a starting point for own developments. It
is not configured to provide product-grade maturity and security.

For further details, see [example image readme](meta-iot2000-example/README.md).
