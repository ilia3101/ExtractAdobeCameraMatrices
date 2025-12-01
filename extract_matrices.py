import sys
import os

try:
    import exifread
except ImportError:
    print("\nExifread not installed. Install it with 'pip3 install exifread'")
    exit()

try:
    from natsort import natsorted, ns
except ImportError:
    natsort_available = False
    print("""\nNatsort module is not installed. It is not necessary, but orders the camera names nicer in the output file.
You can install it with 'pip3 install natsort'""")
else:
    natsort_available = True

def string_to_matrix(string):
    matrix = string.replace("[", "").replace("]", "").split(",")
    for i in range (0,len(matrix)):
        matrix[i] = '%.4f' % eval(matrix[i])
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

def print_matrix_rs(matrix, end):
    mat_str = ("[" + "\n" +
        "\t\t\t[" + ", ".join([x for x in matrix[0:3]]) + " ],\n" +
        "\t\t\t[" + ", ".join([x for x in matrix[3:6]]) + " ],\n" +
        "\t\t\t[" + ", ".join([x for x in matrix[6:9]]) + " ]\n" +
        "\t\t]" + end)
    print(mat_str)

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

if (natsort_available):
    # Natural sort. So that Canon 5D comes first :D
    cameras = natsorted(cameras, key=lambda y: y[0].lower())

################ PRINT the C FILE #################

#Hacky- change stdout to be file
out_file_c = open('camera_matrices.c', 'w')
out_file_rs = open('camera_matrices.rs', 'w')

sys.stdout = out_file_c

print(
"""/* ColorMatrix1 is for illuminant A (tungsten, 2856K)
 * ColorMatrix2 is for illuminant D65 (daylight, 6504K) */
typedef struct {
    char * CameraName;
    double ColorMatrix1[9];
    double ColorMatrix2[9];
} CameraMatrixInfo_t;

CameraMatrixInfo_t all_camera_matrices[] = {""")

for camera_info in cameras:
    print("\t{")
    print ('\t\t"' + camera_info[0].replace("\"", "\\\"") + '",');
    print_matrix(camera_info[1], ",")
    print_matrix(camera_info[2], "")
    print("\t},")

print("};")

out_file_c.close()

sys.stdout = out_file_rs

print(
"""/* ColorMatrix1 is for illuminant A (tungsten, 2856K)
 * ColorMatrix2 is for illuminant D65 (daylight, 6504K) */
#[derive(Clone,Copy)]
pub struct CameraMatrixInfo {
    pub camera_name: &'static str,
    pub color_matrix_1: [[f32; 3]; 3],
    pub color_matrix_2: [[f32; 3]; 3]
}

pub fn get_matrix_for_camera_by_name(cam_name: &str) -> Option<&'static CameraMatrixInfo> {
    for mat in ALL_CAMERA_MATRICES {
        if mat.camera_name == cam_name {
            return Some(mat)
        }
    }
    None
}

pub const ALL_CAMERA_MATRICES: &'static [CameraMatrixInfo] = &[""")

for camera_info in cameras:
    print("\tCameraMatrixInfo {")
    print ('\t\tcamera_name: "' + camera_info[0].replace("\"", "\\\"") + '",');
    print("\t\tcolor_matrix_1: ", end="")
    print_matrix_rs(camera_info[1], ",")
    print("\t\tcolor_matrix_2: ", end="")
    print_matrix_rs(camera_info[2], "")
    print("\t},")

print("];")

out_file_rs.close()
