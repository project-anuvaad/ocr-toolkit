PSM=7
DYNAMIC_MARGINS = False
PERSPECTIVE_TRANSFORM = True

TESS_OCR=True
#if set to None the lang provide in OCR config will be used for psm 6 ocr (when text block contains more than one line) 
FALL_BACK_LANGUAGE=None

C_X=-10
C_Y= 0

#For more info about postprocssing flags rfer the module post_process.py
POST_PROCESSING_MODE = None
#POST_PROCESSING_MODE = 'DoubleOcr'
DOUBLE_OCR_THRESHOLD = 20
DOUBLE_OCR_LANG      =  'Devanagari'
EMPTY_DF_LANG = "Devanagari"
BASE_LANGUAGE = "Devanagari"

TRAINED_EMPTY_DF_LANG = "Devanagari"
TRAINED_LANGUAGE = "Devanagari"


img_path = "/home/srihari/Downloads/scene_text/all_data_combined/hindi/*.png"
txt_path = "/home/srihari/Downloads/scene_text/all_data_combined/hindi/"
save_csv_path = "/home/srihari/Downloads/scene_text/all_data_combined/tesseract_evaluation_csv.csv"