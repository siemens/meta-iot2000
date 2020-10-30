--[[

   Author: Andreas Reichel
           Heiko Schabert
   Copyright (C) 2020, Siemens AG

   SPDX-License-Identifier: GPL-2.0-or-later

]]

local rootindex = -1
local newroot = ""
local envfilename = "envvarlist.txt"
local bootlabels = { "C:BOOT0:", "C:BOOT1:" }
local kernelname = "bzImage"
local kernelparams = "root=/dev/REPLACEME console=ttyS1,115200 earlyprintk"

-- handler for updating root partition
function roundrobin_handler(image)

    -- check if we can chain the raw handler
    if not swupdate.handler["raw"] then
        swupdate.error("raw handler not available")
        return 1
    end

    -- get device list for round robin
    local devlist = {}
    for d in image.device:gmatch("([^,]+)") do
        table.insert(devlist, d)
    end

    if #devlist < 2 then
        swupdate.error("You must specify at least 2 root devices")
        return 1
    end

    kernelparamfile = "/proc/cmdline"
    file = assert(io.open(kernelparamfile, "r"), "Cannot open /proc/cmdline")
    line = ""
    if file then
        line = file:read("*l")
        file:close()
    end
    root = ""
    for param in line:gmatch("%S+") do
        if param:find("root=") then
            root = param:gsub("root=/dev/", "")
            break
        end
    end
    if root == "" then
        swupdate.error("Cannot determin current root")
        return 1
    end
    for idx, dev in ipairs(devlist) do
        if dev == root then
            rootindex = idx
        end
    end
    if rootindex == -1 then
        swupdate.error("Current root device not in the round robin list")
        return 1
    end

    -- perform round robin for update target
    rootindex = rootindex + 1
    if rootindex > #devlist then
        rootindex = 1
    end

    newroot = devlist[rootindex]
    swupdate.debug("using " .. newroot .. " as target")

    image.type = "raw"
    image.device = "/dev/" .. newroot
    local err, msg = swupdate.call_handler("raw", image)
    if err ~= 0 then
        swupdate.error("Error calling raw handler: " .. (msg or ""))
        return 1
    end
    return 0
end

-- handler for updating kernel file
function kernel_handler(image)

    -- check if we can chain the rawfile handler
    if not swupdate.handler["rawfile"] then
        swupdate.error("rawfile handler not available")
        return 1
    end

    if rootindex == -1 then
        swupdate.error("please use the roundrobin-handler before the kernel-handler in your sw-description")
        return 1
    end

    -- get device list for round robin
    devlist = {}
    for d in image.device:gmatch("([^,]+)") do
        table.insert(devlist, d)
    end

    if rootindex > #devlist then
        swupdate.error("Could not map kernel partition to root partition: not enough kernel partitions to chose from.")
        return 1
    end

    swupdate.debug("Using kernel partition " .. (devlist[rootindex] or ""))

    image.device = "/dev/" .. devlist[rootindex]
    local err, msg = swupdate.call_handler("rawfile", image)
    if err ~= 0 then
        swupdate.error("Error calling raw file handler: " .. (msg or ""))
        return 1
    end


    -- update the bootloader
    kernelparams = kernelparams:gsub("REPLACEME", newroot)
    kernelfile = bootlabels[rootindex] .. kernelname

    swupdate.info("Setting bootloader environment: %s=%s", "kernelfile", kernelfile)
    swupdate.set_bootenv("kernelfile", kernelfile)

    swupdate.info("Setting bootloader environment: %s=%s", "kernelparams", kernelparams)
    swupdate.set_bootenv("kernelparams", kernelparams)

    return 0
end

swupdate.register_handler("roundrobin", roundrobin_handler, swupdate.HANDLER_MASK.IMAGE_HANDLER)
swupdate.register_handler("kernel", kernel_handler, swupdate.HANDLER_MASK.FILE_HANDLER)
