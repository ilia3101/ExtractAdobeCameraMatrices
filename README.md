# ExtractAdobeCameraMatrices
Extract camera matrices from Adobe profiles

Dependencies:
- `exifread` and `natsort` python libraries from pip
- `7z` command, provided by `p7zip-full` package on Ubuntu

Instructions:
1. Download latest DNG converter executable for Windows
2. Run: `./extract.sh path_to_dng_converter.exe`
3. Enjoy your matrices in the output file`camera_matrices.c`