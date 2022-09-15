# import logging
DEBUG = False
API_URL_PREFIX = "/tarento/"
HOST = "0.0.0.0"
PORT = 5000
BASE_DIR = 'upload'

ENABLE_CORS = False
IS_DYNAMIC = True
EXRACTION_RESOLUTION = 300


OUTPUT_SAVE_DIR="output/"
LANG_MAPPING = {
    "en": ["Latin", "eng"],
    "kn": ['Kannada', "kan"],
    "gu": ["Gujrati", "guj"],
    "or": ["Oriya", "ori"],
    "hi": ["Devanagari", "hin"],
    "bn": ["Bengali", "ben"],
    "mr": ["Devanagari", "mar"],
    "ta": ['Tamil', "tam"],
    "te": ["Telugu", "tel"],
    "ml": ["Malayalam", "mal"],
    "ma": ["Marathi", "mar"],
    "pa": ["Punjabi", "pun"],
}


LINE_PRIMA_SCORE_THRESH_TEST = 0.50
LINE_DETECTION=True

LINE_LAYOUT_MODEL_PATH = "./src/utilities/primalinenet/passport_roi_v1.pth"
LINE_LAYOUT_CONFIG_PATH = "./src/utilities/primalinenet/passport_roi_v1_config.yaml"
##########################################################################
# Alignment
EAST_MODEL = "./src/utilities/east/frozen_east_text_detection.pb"
ANGLE_TOLLERANCE  = 0.25
MIN_CONFIDENCE    = 0.5
MARGIN_TOLLERANCE = 9
EAST_WIDTH        = 1280
EAST_HEIGHT       = 1280
ALIGN = False
ALIGN_MODE = 'FAST'
### image superesolution
SUPER_RESOLUTION=False
SUPER_RES_MODEL="./src/utilities/superres/sr_model.hdf5"

### ocr config
BATCH_SIZE = 1
DYNAMIC_MARGINS = False
PERSPECTIVE_TRANSFORM = True
FALL_BACK_LANGUAGE = None
PSM = 7
POST_PROCESSING_MODE = None
MULTIPROCESS = False
MASK_OUT=False

DRAW_BOX=True
CROP_SAVE=True
SAVE_PATH_BOX="draw_sample/"
CROP_SAVE_PATH="draw_crop_sample/"
LOCAL_IMG_PATH="./input/"

# crop config
C_X = -7
C_Y = 0

