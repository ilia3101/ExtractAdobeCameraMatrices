#!/bin/bash

mkdir exefiles
7z x $1 -y -oexefiles

python3 extract_matrices.py 'exefiles/$APPDATA/Adobe/CameraRaw/CameraProfiles/Adobe Standard' > camera_matrices.c