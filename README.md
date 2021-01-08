## Extract camera matrices from Adobe profiles

Dependencies:
- `exifread` and `natsort` python libraries from pip
- `7z` command, provided by `p7zip-full` package on Ubuntu

Instructions:
1. Download the latest [Adobe DNG Converter for Windows](https://www.adobe.com/go/dng_converter_win/)
2. Run `./extract.sh path_to_downloaded_dng_converter.exe`
3. Find the matrices in `camera_matrices.c`, which the script will have created
