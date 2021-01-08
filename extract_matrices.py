import exifread
import sys
import os
from natsort import natsorted, ns

def string_to_matrix(string):
    matrix = string.replace("[", "").replace("]", "").split(",")
    for i in range (0,len(matrix)):
        matrix[i] = str(eval(matrix[i]))
    return matrix

def get_camera_matrices(filename):
    camera_name = None
    colormatrix1 = None
    colormatrix2 = None
    f = open(filename, 'rb')
    tags = exifread.process_file(f)

    for tag in tags.keys():
        if ('0xC614' in tag):
            camera_name = str(tags[tag])
        if ('0xC621' in tag):
            colormatrix1 = string_to_matrix(str(tags[tag]))
        if ('0xC622' in tag):
            colormatrix2 = string_to_matrix(str(tags[tag]))
    return (camera_name, colormatrix1, colormatrix2)

def print_matrix(matrix, end):
    print("\t\t{ " + ", ".join(matrix) + " }" + end)

profile_dir = sys.argv[1]
profile_files = sorted(os.listdir(profile_dir))

cameras=[]

for profile_file in profile_files:
    if ('.dcp' in profile_file):
        camera_info = get_camera_matrices(profile_dir+"/"+profile_file)
        # make sure profile contains everything and camera has 3x3 matrix (ignore 4 channel cameras yes, this is a TODO)
        if (camera_info[0] != None and camera_info[1] != None and
            camera_info[2] != None and len(camera_info[1]) == 9):
            cameras.append(camera_info)

# Natural sort. So that Canon 5D comes first :D
cameras = natsorted(cameras, key=lambda y: y[0].lower())

################ PRINT the C FILE #################

print(
"""typedef struct {
    char * CameraName;
    double ColorMatrix1[9];
    double ColorMatrix2[9];
} CameraMatrixInfo_t;

CameraMatrixInfo_t all_camera_matrices[] = {""")

for camera_info in cameras:
    print("\t{")
    print ('\t\t"' + camera_info[0] + '",');
    print_matrix(camera_info[1], ",")
    print_matrix(camera_info[2], "")
    print("\t},")

print("};")