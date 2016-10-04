#!/bin/sh
#Krzysztof.M.Sywula@intel.com

SKETCH=/sketch
SKETCH_SIZE=256 #KB
ERASE_SIZE=32 #KB
IMAGE=/opt/cln/galileo/jffs2.bin
DEVICE=/dev/mtdblock0

start()
{
	dd if=$IMAGE of=$DEVICE
	mount -t jffs2 $DEVICE $SKETCH
}

stop()
{
	umount $SKETCH
	dd if=$DEVICE of=$IMAGE
}

setup()
{
	ulimit -c unlimited
	modprobe mtdram total_size=$SKETCH_SIZE erase_size=$ERASE_SIZE
	modprobe mtdchar
	modprobe mtdblock
	mkdir -p $SKETCH
	
	# IF IMAGE DOES NOT EXIST - CREATE ONE
	test -f $IMAGE || mkfs.jffs2 --pad=$(($SKETCH_SIZE * 1024)) -r /tmp --eraseblock=$ERASE_SIZE -o $IMAGE
}

usage()
{
	echo "Use: $1 [start/stop]"
	exit 1
}

main()
{
	echo $1
	if [ "x$1" = "xstart" ]; then
	#	setup
	#	start
		mkdir -p /sketch
	elif [ "x$1" = "xstop" ]; then
	#	stop
	else
		usage $0
	fi
}

main "$@"
