#!/bin/bash

mkdir exefiles
cd exefiles
innoextract $1
cd ../
python3 extract_matrices.py 'exefiles/commonappdata/Adobe/CameraRaw/CameraProfiles/Adobe Standard'
rm -rf exefiles