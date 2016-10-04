#!/bin/sh
GALILEO_PATH="/opt/cln/galileo"
CLLOADER="$GALILEO_PATH/clloader"
CLLOADER_OPTS="--escape --binary --zmodem --disable-timeouts"
SKETCH_RESET="$GALILEO_PATH/galileo_sketch_reset"

mytrap()
{
  kill -KILL $clPID
  keepgoing=false
}

trap 'mytrap' USR1

arduino_services()
{
  $SKETCH_RESET $sketch_reset_params &

  keepgoing=true
  while $keepgoing
  do
      $CLLOADER $CLLOADER_OPTS < /dev/ttyGS0 > /dev/ttyGS0 & clPID=$!
      wait $clPID
      usleep 200000
  done
}

sketch_reset_params="-i 63 -o 47"
arduino_services
