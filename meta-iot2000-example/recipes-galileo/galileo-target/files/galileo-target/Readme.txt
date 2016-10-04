This is the izmir download daemon.

It needs to be built with the yocto Linux cross compiler, not the cross compiler for sketches.
Compiler was setup using: 
source /nfs/iir/disks/clanton_disk005/users/software/linux_xcompiler/1.4.1/environment-setup-i586-poky-linux-uclibc


Run the command on the target:
./clloader --escape --binary < /dev/ttyGS0 > /dev/ttyGS0

clloader --help for other options.

Clloader will look for /sketch/sketch.elf and run it if found.
Output from the sketch will be redirected back to /dev/ttyGS0

If clloader is HUPed while running a sketch it will terminate the sketch and wait for a command.   
If the sketch terminates the loader will revert back to waiting for a remote command.   



