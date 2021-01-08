## Extract camera matrices from Adobe profiles

This program extracts ColorMatrix1 and ColorMatrix2 from every DCP profile included in Adobe DNG converter.
ColorMatrix1 is for illuminant A (tungsten, 2856K) ColorMatrix2 is for illuminant D65 (daylight, 6504K).
This might be useful if you are making a raw converter or software that deals with raw photos.

### Dependencies
- `exifread` and `natsort` python libraries from pip
- `7z` command, provided by `p7zip-full` package on Ubuntu

### Instructions
1. Download latest DNG converter executable for Windows
2. Run: `./extract.sh path_to_dng_converter.exe`
3. Enjoy your matrices in the output file `camera_matrices.c`
