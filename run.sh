#!/usr/bin/env bash
BASEDIR=$( realpath "$0"  ) && dirname "$BASEDIR"
FOLDER=`dirname $BASEDIR`
UI_PATH="$FOLDER/UI.py"
python "$UI_PATH"
# F:/anaconda3/python.exe "$UI_PATH"