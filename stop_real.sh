#!/bin/bash
cd `dirname "$0"`/pid

GAME=game.pid


if [ -e $GAME ]; then
    kill `cat $GAME`
    echo "Stopped Server ... PID: $PWD/$GAME"
fi
