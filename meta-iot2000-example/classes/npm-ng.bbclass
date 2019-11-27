# Copyright (c) Siemens AG, 2018
#
# SPDX-License-Identifier: MIT

# HOWTO generate an npm-shrinkwrap.json:
#   npm install --global-style <my-favorite-package>
#   cp package-lock.json /path/to/recipe/files/npm-shrinkwrap.json

NPMPN ?= "${PN}"
NPM_SHRINKWRAP ?= "file://npm-shrinkwrap.json"
NPM_LOCAL_INSTALL_DIR ?= ""

NPM_REBUILD ?= "1"

SRC_URI = "npm://registry.npmjs.org;name=${NPMPN};version=${PV} \
    ${NPM_SHRINKWRAP}"

# function maps arch names to npm arch names
def npm_oe_arch_map(target_arch, d):
    import re
    if   re.match('p(pc|owerpc)(|64)', target_arch): return 'ppc'
    elif re.match('i.86$', target_arch): return 'ia32'
    elif re.match('x86_64$', target_arch): return 'x64'
    elif re.match('arm64$', target_arch): return 'arm'
    return target_arch

NPM_ARCH ?= "${@npm_oe_arch_map(d.getVar('TARGET_ARCH'), d)}"

python() {
    src_uri = (d.getVar('SRC_URI', True) or "").split()
    if len(src_uri) == 0:
        return

    new_src_uri = []
    npm_uri = None
    for u in src_uri:
        if u.startswith("npm://"):
            if npm_uri:
                bb.fatal("Only one npm package per recipe supported")
            npm_uri = u
        else:
            new_src_uri.append(u)

    d.setVar('SRC_URI', ' '.join(new_src_uri))
    d.setVar('NPM_URI', npm_uri)

    type, host, path, user, pswd, params = bb.fetch2.decodeurl(npm_uri)

    if params['version'] != d.getVar('PV'):
        bb.fatal("Mismatch between PV and version stored in registry")

    d.setVar('NPM_REGISTRY', "https://" + host)

    mapped_name = params['name']
    if mapped_name.startswith('@'):
        mapped_name = mapped_name[1:].replace('/', '-')
    d.setVar('NPM_MAPPED_NAME', mapped_name)
}

def get_npm_bundled_tgz(d):
    return "%s/%s-%s-bundled.tgz" % \
        (d.getVar('DL_DIR'), d.getVar('NPM_MAPPED_NAME'), d.getVar('PV'))

def runcmd(cmd):
    import subprocess
    (retval, output) = subprocess.getstatusoutput(cmd)
    if retval:
        bb.fatal("Failed to run '%s'%s" % \
            (cmd, ":\n%s" % output if output else ""))
    bb.note(output)

NPM_FETCH_TMP = "${WORKDIR}/fetch-tmp"

python fetch_npm() {
    import json, os, shutil

    workdir = d.getVar('WORKDIR');
    tmpdir = d.getVar('NPM_FETCH_TMP')
    shrinkwarp_url = d.getVar('NPM_SHRINKWRAP')

    try:
        fetch = bb.fetch2.Fetch([shrinkwarp_url], d)
        fetch.unpack(workdir)
    except bb.fetch2.BBFetchException as e:
        bb.fatal(str(e))

    shrinkwarp_path = fetch.localpath(shrinkwarp_url)
    filelist = shrinkwarp_path + ":True"
    checksum_list = bb.fetch2.get_file_checksums(filelist, d.getVar('PN'))
    _, shrinkwarp_chksum = checksum_list[0]

    bundled_tgz = get_npm_bundled_tgz(d)
    bundled_tgz_hash = bundled_tgz + ".hash"

    fetch_hash = d.getVar('NPM_URI') + "\n" + \
        shrinkwarp_url + " " + shrinkwarp_chksum + "\n"

    if os.path.exists(bundled_tgz) and os.path.exists(bundled_tgz_hash):
        with open(bundled_tgz_hash) as hash_file:
            hash = hash_file.read()
        if hash == fetch_hash:
            return

    old_cwd = os.getcwd()
    os.chdir(tmpdir)

    shutil.copyfile(shrinkwarp_path, "npm-shrinkwrap.json")

    # changing the home directory to the tmpdir directory, the .npmrc will
    # be created in this directory
    os.environ['HOME'] = tmpdir

    os.environ.update({'npm_config_registry': d.getVar('NPM_REGISTRY')})
    bb.utils.export_proxies(d)

    npmpn = d.getVar('NPMPN')

    with open("package.json", 'w') as outfile:
        json_objs = {'dependencies': { npmpn: '' }}
        json.dump(json_objs, outfile, indent=2)

    runcmd("npm ci --global-style --ignore-scripts --verbose")

    os.chdir("node_modules/" + npmpn)

    with open("package.json") as infile:
        json_objs = json.load(infile)

    deps = [d for d in json_objs['dependencies']]
    json_objs.update({'bundledDependencies': deps})

    # update package.json so that all dependencies are bundled
    with open("package.json", 'w') as outfile:
        json.dump(json_objs, outfile, indent=2)

    runcmd("npm pack --ignore-scripts --verbose")

    shutil.copyfile("%s-%s.tgz" % (d.getVar('NPM_MAPPED_NAME'), d.getVar('PV')),
                    bundled_tgz)
    with open(bundled_tgz_hash, 'w') as hash_file:
        hash_file.write(fetch_hash)

    os.chdir(old_cwd)
}
do_fetch[postfuncs] += "fetch_npm"
do_fetch[cleandirs] += "${NPM_FETCH_TMP}"

python clean_npm() {
    import os

    bundled_tgz = get_npm_bundled_tgz(d)
    if os.path.exists(bundled_tgz):
        os.remove(bundled_tgz)

    bundled_tgz_hash = bundled_tgz + ".hash"
    if os.path.exists(bundled_tgz_hash):
        os.remove(bundled_tgz_hash)
}
do_cleanall[postfuncs] += "clean_npm"

S = "${WORKDIR}/npmpkg"

unpack_npm() {
    tar xzf ${@get_npm_bundled_tgz(d)} -C ${S} --strip-components=1
}
do_unpack[postfuncs] += "unpack_npm"

DEPENDS += "nodejs-native"

do_compile() {
    # changing the home directory to the working directory, the .npmrc will
    # be created in this directory
    export HOME=${WORKDIR}

    # ensure empty cache
    export npm_config_cache=${WORKDIR}/npm_cache

    export npm_config_nodedir=${RECIPE_SYSROOT_NATIVE}/usr/

    INSTALL_FLAGS="--offline --only=production --no-package-lock --verbose \
                   --arch=${NPM_ARCH} --target_arch=${NPM_ARCH}"

    if [ -n "${NPM_LOCAL_INSTALL_DIR}" ]; then
        mkdir -p ${WORKDIR}/installed/${NPM_LOCAL_INSTALL_DIR}
        cd ${WORKDIR}/installed/${NPM_LOCAL_INSTALL_DIR}
    else
        INSTALL_FLAGS="$INSTALL_FLAGS --prefix ${WORKDIR}/installed/${prefix} -g"
    fi

    if [ -n "${NPM_REBUILD}" ]; then
        INSTALL_FLAGS="$INSTALL_FLAGS --build-from-source"
    fi

    npm install $INSTALL_FLAGS ${@get_npm_bundled_tgz(d)}

    if [ -d ${WORKDIR}/installed/${libdir}/node_modules ]; then
        mv ${WORKDIR}/installed/${libdir}/node_modules \
           ${WORKDIR}/installed/${libdir}/node
    fi
}
do_compile[cleandirs] += " \
    ${WORKDIR}/npm_cache \
    ${WORKDIR}/installed"

do_install() {
    cp -a --no-preserve=ownership ${WORKDIR}/installed/* ${D}/
}

def get_nodes_install_dir(d):
    npm_local_install_dir = d.getVar('NPM_LOCAL_INSTALL_DIR')
    if npm_local_install_dir != "":
        return npm_local_install_dir + "/node_modules"
    else:
        return d.getVar('libdir') + "/node"

FILES_${PN} += "${@get_nodes_install_dir(d)}/${NPMPN}"
