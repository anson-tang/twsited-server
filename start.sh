#!/bin/bash

cd `dirname "$0"`
LOGDIR=$PWD/logs
PIDDIR=$PWD/pid
UMASK=022
. setup_env.sh

echo "Starting Server... PID: $PIDDIR/game.pid "
twistd -repoll --pidfile $PIDDIR/game.pid -l $LOGDIR/game.log --umask=$UMASK -y $PWD/gameserver/main.py

