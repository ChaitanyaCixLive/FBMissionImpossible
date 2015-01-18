#!/bin/bash

BASEDIR=$(dirname $0)

PATH=$BASEDIR:/usr/lib/lightdm/lightdm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

echo "Updating movie list"

cd $BASEDIR

python MissionImpossible.py
