import os

path = os.getcwd()
path = '/home/ronal/Documents/willems'
#TODO

DATASET_FOLDER =os.path.normpath(path+'/datasetImg') + '/'
PICKLE_FOLDER = os.path.normpath(path+'/datasetPickle') + '/'
MODEL_FOLDER =  os.path.normpath(path+'/datasetModel') + '/'
PATH_TESTING =os.path.normpath(path+'/datasetTesting') + '/'

TOOTH_JSON_PATH =           os.path.normpath(path+'/datasetJson/tooth.json')
AGE_PREDICTION_JSON_PATH =  os.path.normpath(path+'/datasetJson/agePrediction.json')
RESULT_JSON_PATH =          os.path.normpath(path+'/datasetJson/result.json')

CROP_FILE_NAME = 'crop'
NO_IMAGES_FILE_NAME = 'No Images'
NO_IMAGE_FILE_NAME = 'No Image'
IMAGE_TYPE = '.jpg'
IMAGE_SIZE = 64
ASCII_A = 65
THRESHOLD = 0.3
EPOCHS = 5

class buttonLabel():
    LOAD_IMAGE =    'Load Image'
    CROP_IMAGE =    'Region'
    SELECT_REGION = 'Pilih Gigi'
    PREDICT =       'Estimasi'
    RESET_IMAGE =   'Reset'

class region():
    CENTRAL_INCISOR = 'Central Incisor'
    LATERAL_INCISOR = 'Lateral Incisor'
    CANINE =          'Canine'
    FIRST_PREMOLAR =  'First Premolar'
    SECOND_PREMOLAR = 'Second Premolar'
    FIRST_MOLAR =     'First Molar'
    SECOND_MOLAR =    'Second Molar'

class gender():
    MALE =   'Laki-Laki'
    FEMALE = 'Perempuan'

# Show/Hide TabMenu
class hideFrame():
    hideFrameStatus = False
    hideFrameInformation = False
    hideFrameProfile = True

class pesan():
    SIMPAN_STAGE = 'Simpan stage ini sebagai Region '
    ERR_KESALAHAN = 'Terjadi Kesalahan!'
    LABEL_MESSAGE = 'Status          : '
    LABEL_IMAGE_PATH = 'Path            : '
    LABEL_STATUS_PROCESS = 'Status Process  : '
    LABEL_STATUS_PREDICT = 'Status Estimasi : '
    FRAME_STATUS = 'Status'
    FRAME_INFORMATION = 'Information'
    FRAME_PROFILE = 'Profile'
    TITLE = 'Tooth Clasification'
    OPEN_AND_PUT = 'Load Data'
    RESET_IMAGE = 'Reset Image'
    CREATE_IMAGE = 'Create Image'
    BUTTON_PRESS = 'Mouse Click : '
    BUTTON_MOVE = 'Mouse Move x : '
    BUTTON_RELEASE = 'Mouse Release'
    SAVE_IMAGE = 'Save Image'
    SAVE_REGION = 'Tooth {} Selected'
    SAVE_CROP = 'Region Crop Finish'
    IMAGE = 'Image'
    UMUR = '\n\nTahun'
    SELECTED = 'Selected'
    PREDICT1 = 'Mencoba Mengestimasi '
    PREDICT2 = 'Berhasil Mengestimasi'
    FINAL_RESULT = 'Anak {} dengan umur {} tahun'
    SELECT = 'Select Gambar'
    CROP = 'Crop Gambar'
    THRESHOLD = 'Deviasi   : '
    MAX_THRESHOLD = 'Max Predict : '
    MIN_THRESHOLD = 'Min Predict : '
    COPY_RIGHT = 'Copyright © Michael Saelung 2022'
    TOOTH = """
                                 A      B     C     D     E     F     G     H
    BOY  :  Central Incisor  :   0.00   0.00  1.68  1.49  1.50  1.86  2.07  2.19
            Lateral Incisor  :   0.00   0.00  0.55  0.63  0.74  1.08  1.32  1.64
            Canine           :   0.00   0.00  0.00  0.04  0.31  0.47  1.09  1.90
            First Premolar   :   0.15   0.56  0.75  1.11  1.48  2.03  2.43  2.83
            Second Premolar  :   0.08   0.05  0.12  0.27  0.33  0.45  0.40  1.15
            First Molar      :   0.00   0.00  0.00  0.69  1.14  1.60  1.95  2.15
            Second Molar     :   0.18   0.48  0.71  0.80  1.31  2.00  2.48  4.17
    GIRL :  Central Incisor  :   0.00   0.00  1.83  2.19  2.34  2.82  3.19  3.14
            Lateral Incisor  :   0.00   0.00  0.00  0.29  0.32  0.49  0.79  0.90
            Canine           :   0.00   0.00  0.60  0.54  0.62  1.08  1.72  2.00
            First Premolar   :  -0.95  -0.15  0.16  0.41  0.60  1.27  1.58  2.19
            Second Premolar  :  -0.19   0.01  0.27  0.17  0.35  0.35  0.55  1.51
            First Molar      :   0.00   0.00  0.00  0.62  0.90  1.56  1.82  2.21
            Second Molar     :   0.14   0.11  0.21  0.32  0.66  1.28  2.09  4.04
            """
    PROFILE = """
    Nama         : Michael Saelung Sinambela
    Alamat       :
    Fakultas     :
    Bidang Studi :
              """