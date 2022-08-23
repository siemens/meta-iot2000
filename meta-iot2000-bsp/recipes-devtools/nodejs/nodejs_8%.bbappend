FILESEXTRAPATHS_prepend := "${THISDIR}/nodejs:"

SRC_URI += " \
    file://0001-Restore-x87-port.patch \
    file://0002-Switch-to-x87-mode-when-targeting-ia32.patch \
    file://0003-Relax-check-in-ComputeInputFrameSize.patch \
    file://0004-py2to3-automatic-conversion-via-2to3-tool.patch \
    file://0005-py2to3-fix-configure.patch \
    file://0006-py2to3-fix-tools-gyp-pylib-gyp-input.py.patch \
    file://0007-py2to3-fix-tools-configure.d-nodedownload.py.patch \
    file://0008-py2to3-deps-v8-gypfiles-toolchain.gypi.patch \
    file://0009-py2to3-fix-tools-gyp-pylib-gyp-generator-make.py.patch \
    file://0010-py2to3-fix-tools-compress_json.py.patch \
    file://0011-py2to3-fix-tools-js2c.py-deps-v8-tools-js2c.py.patch \
    file://0012-py2to3-fix-deps-v8-tools-gen-postmortem-metadata.py.patch \
    file://0013-py2to3-fix-async-keyword-error.patch \
    file://0014-py2to3-fix-deps-v8-third_party-jinja2-runtime.py.patch \
    file://0015-py2to3-fix-gyp-samples-samples.patch \
    file://0016-py2to3-use-python3-for-node-gyp.patch \
    file://0017-CVE-2019-15606.patch \
    file://0018-CVE-2019-15604.patch \
    file://0019-CVE-2019-15605.patch \
    file://0020-CVE-2020-8174.patch \
    file://0021-nghttp2_1.41.0.patch \
    file://0022-CVE-2020-11080.patch \
    file://0023-CVE-2020-8265.patch \
    file://0024-CVE-2020-8287.patch \
    file://0025-CVE-2021-22884.patch \
    file://0026-CVE-2021-22883.patch \
    file://0027-CVE-2021-22930.patch \
    file://0028-CVE-2021-22939.patch \
    file://0029-CVE-2021-44907.patch \
    file://0030-CVE-2022-0235.patch \
    file://0031-OpenSSL-1.1.1-support.patch \
    file://0032-Fix-build-with-openssl-1.1.1d.patch \
"
