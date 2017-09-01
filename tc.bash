#!/bin/bash
#
#  tc uses the following units when passed as a parameter.
#  kbps: Kilobytes per second
#  mbps: Megabytes per second
#  kbit: Kilobits per second
#  mbit: Megabits per second
#  bps: Bytes per second
#       Amounts of data can be specified in:
#       kb or k: Kilobytes
#       mb or m: Megabytes
#       mbit: Megabits
#       kbit: Kilobits
#  To get the byte figure from bits, divide the number by 8 bit
#

#
# Name of the traffic control command.
TC=/sbin/tc

# The network interface we're planning on limiting bandwidth.
IF=eth1             # Interface

# Download limit (in mega bits)
#DNLD=${2:4}         # DOWNLOAD Limit

# Upload limit (in mega bits)
UPLD=${2:3}         # UPLOAD Limit

# Delay limit (in ms)
#DELAY=${3:6}

# Packet loss (in %)
#LOSS=${4:5}

# IP address of the machine we are controlling
IP=192.168.0.3     # Host IP

# Filter options for limiting the intended interface.
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

start() {

# We'll use Hierarchical Token Bucket (HTB) to shape bandwidth.
# For detailed configuration options, please consult Linux man
# page.

    $TC qdisc add dev $IF root handle 1: htb default 30 
    #$TC class add dev $IF parent 1: classid 1:1 htb rate $DNLD
    $TC class add dev $IF parent 1: classid 1:2 htb rate $UPLD
    #$TC qdisc add dev $IF parent 1:2 handle 10: netem delay $DELAY
    #$TC qdisc change dev $IF parent 1:2 handle 10: netem loss $LOSS

    #$U32 match ip dst $IP/32 flowid 1:1
    $U32 match ip src $IP/32 flowid 1:2

# The first line creates the root qdisc, and the next two lines
# create two child qdisc that are to be used to shape download
# and upload bandwidth.
#
# The 4th and 5th line creates the filter to match the interface.
# The 'dst' IP address is used to limit download speed, and the
# 'src' IP address is used to limit upload speed.

}

stop() {

# Stop the bandwidth shaping.
    $TC qdisc del dev $IF root

}

restart() {

# Self-explanatory.
    stop
    sleep 1
    start

}

update() {

# Self-explanatory.
    if [ $UPLD != "0" ];
    then $TC class change dev $IF parent 1: classid 1:2 htb rate $UPLD;
    fi

   # $TC class change dev $IF parent 1: classid 1:1 htb rate $DNLD
   # if [ $DELAY != "0" ]; 
   # then $TC qdisc change dev $IF parent 1:2 handle 10: netem delay $DELAY;
   # fi

   # if [ $LOSS != "0" ];
   # then $TC qdisc change dev $IF parent 1:2 handle 10: netem loss $LOSS;
   # fi
}

upload() {
    $TC class change dev $IF parent 1: classid 1:2 htb rate $UPLD
}

delay() {
    $TC qdisc change dev $IF parent 1:2 handle 10: netem delay $DELAY
}

show() {

# Display status of traffic control status.
    $TC -s qdisc ls dev $IF

}

case "$1" in

  start)

    echo -n "Starting bandwidth shaping: "
    start
    echo "done"
    ;;

  stop)

    echo -n "Stopping bandwidth shaping: "
    stop
    echo "done"
    ;;

  restart)

    echo -n "Restarting bandwidth shaping: "
    restart
    echo "done"
    ;;

  update)

   #echo -n "Updating bandwidth shaping: "
   update
   #echo "done"
   ;;

   delay)

   echo -n "Delaying bandwidth shaping: "
   delay
   echo "done"
   ;;

   upload)

   echo -n "Setting upload shaping: "
   upload
   echo "done"
   ;;

  show)

    echo -n "Bandwidth shaping status for $IF:"
    show
    echo ""
    ;;

  *)

    pwd=$(pwd)
    echo "Usage: tc.bash {start|stop|restart|update|delay|show}"
    ;;

esac

exit 0
