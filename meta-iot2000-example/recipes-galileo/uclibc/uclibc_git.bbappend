#
# Copyright (c) Siemens AG, 2016
#
# Authors:
#  Claudius Heine <ch@denx.de>
#
# This file is subject to the terms and conditions of the MIT License.  See
# COPYING.MIT file in the top-level directory.

FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

# I got the libstdc++.so.* and libgcc_s.so.* by compiling them
# with TCLIB="uclibc" and extracted the libstdc++6*.ipk and libgcc1*.ipk with
# "ar x *.ipk" and then data.tar.gz with "tar xf ..."
SRC_URI_append = " \
    file://0001-dl-elf.c-never-look-in-shared-library-loader-for-lib.patch \
    file://0002-Very-hacky-solution-for-arduino-eeprom-compatibility.patch \
    file://config.cfg \
    file://libstdc++.so.6.0.21 \
    file://libgcc_s.so.1 \
    "

COMPATIBLE_HOST = ".*"

PROVIDES = ""

INSTDIR = "/opt/uclibc"

base_prefix="${INSTDIR}"

python (){
    configmangle = d.getVar('configmangle', True)
    configmangle = configmangle.replace('RUNTIME_PREFIX=\"/\"',
                                        'RUNTIME_PREFIX=\"${INSTDIR}\"')
    configmangle = configmangle.replace('DEVEL_PREFIX=\"/%s\"' % d.getVar('prefix', True),
                                        'DEVEL_PREFIX=\"${INSTDIR}/${prefix}\"')
    configmangle = configmangle.replace('SHARED_LIB_LOADER_PREFIX=\"/lib\"',
                                        'SHARED_LIB_LOADER_PREFIX=\"${INSTDIR}/lib\"')
    d.setVar('configmangle', configmangle)

    d.renameVar('FILES_ldd', 'FILES_%s-ldd' % d.getVar('PN', True))
    packages = d.getVar('PACKAGES', True)
    packages = packages.replace('ldd', '%s-ldd' % d.getVar('PN', True))
    d.setVar('PACKAGES', packages)

    instdir = d.getVar('INSTDIR', True)
    # Change FILES_${PN}-* Variables:
    for sub in ['gconv', 'dev', 'bin',
                'doc', 'locale', 'utils',
                'staticdev', 'ldd', None]:
        varname = 'FILES_%s' % d.getVar('PN', True)
        if sub:
            varname += '-%s' % sub
        var = d.getVar(varname, True)
        #print(d.keys())
        #print(varname, var)
        var = ' '.join(["${INSTDIR}" + s if not s.startswith(instdir) else s for s in var.split()])
        d.setVar(varname, var)
}

do_install_append() {
    ln -s libm.so.1 "${D}${INSTDIR}/lib/libm.so.0"
    ln -s libc.so.1 "${D}${INSTDIR}/lib/libc.so.0"
    ln -s libpthread.so.1 "${D}${INSTDIR}/lib/libpthread.so.0"
    install -m 644 "${WORKDIR}/libstdc++.so.6.0.21" "${D}${INSTDIR}/usr/lib"
    install -m 644 "${WORKDIR}/libgcc_s.so.1" "${D}${INSTDIR}/lib"
    ln -s libstdc++.so.6.0.21 "${D}${INSTDIR}/usr/lib/libstdc++.so.6"
}

PRIVATE_LIBS_${PN}-libcrypt = "libcrypt.so.1"
PRIVATE_LIBS_${PN}-libnsl = "libnsl.so.1"
PRIVATE_LIBS_${PN}-librt = "librt.so.1"
PRIVATE_LIBS_${PN}-libutil = "libutil.so.1"

FILES_${PN}-binlibs = "${INSTDIR}/lib/libgcc_s.so* ${INSTDIR}/usr/lib/libstdc++.so*"
PRIVATE_LIBS_${PN}-binlibs = "libstdc++.so.6.0.21 libstdc++.so.6 libgcc_s.so.1"

PACKAGES_append = " ${PN}-binlibs"

INSANE_SKIP_${PN} += "already-stripped"
INSANE_SKIP_${PN}-binlibs += "build-deps"

export V="1"
