import logging
import sys
logging.basicConfig(level=logging.INFO, filename='tesseract.logs', format='%(asctime)s-%(levelname)s-%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


#The output csv will cotatin a column  'exp' which will have the vlaue  : EXP_NAME_LANG_WEIGHT
EXP_NAME = 'GOOGLE_OCR_15_HINDI_GOOGLE'
LINE_IMAGE_OCR=False

#Will save the intermediate image crops in the output dir
CHECK=True
CROP_SAVE=True
CROP_PATH="/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/crops/hindi"


#Number of parallel tesseract processes to fork 
BATCH_SIZE=10
MAX_QUEUE_SIZE = 100


# i/o dirs
#GT_SOURCE  = '/home/dhiraj/Documents/data/tess_training/iise_gt/iit_line_mapped/101/*/*.csv'
#IMAGE_DIR= '/home/dhiraj/Documents/data/tess_training/iise_gt/IIIT_Hindi_100-20210531T041306Z-001/IIIT_Hindi_100/Images'
#IMAGE_FORMAT='jpg'
#OUTPUT_DIR = '/home/dhiraj/Documents/data/tess_training/scrits/output'
#OUTPUT_FILE = '/home/dhiraj/Documents/data/tess_training/iise_gt/benchmark/test.csv'

# GT_SOURCE = '/home/dhiraj/Documents/data/tess_training/batch_2/output/csv/*'
# IMAGE_DIR  = '/home/dhiraj/Documents/data/tess_training/batch_2/output/images'
# IMAGE_FORMAT ='png'
# OUTPUT_DIR = '/home/dhiraj/Documents/data/tess_training/scrits/output'
# OUTPUT_FILE = '/home/dhiraj/Documents/data/tess_training/iise_gt/benchmark/test_1.csv'

GT_SOURCE = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/csv/*.csv'
IMAGE_DIR  = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/images'
IMAGE_FORMAT ='png'
OUTPUT_DIR = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json'

#OUTPUT_FILE = '/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/report_with_dynamic_margins.csv'
OUTPUT_FILE = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/ulca_report_hindi_benchmark_data_google_lines.csv'



# OCR  config
#LANGUAGES=['ori_v11.795_53317']
#LANGUAGES=['Telugu']
#LANGUAGES=['mal_v10.806_86009']
LANGUAGES=['Devanagari']
#LANGUAGES=['mar_v11.002_65489']
#LANGUAGES=['hin_v50.731_45301']
#LANGUAGES=['kan_v10.519_62976']
#LANGUAGES=['tam_v90.923_39551']
#LANGUAGES=['mar_v11.247_60691']
#LANGUAGES=['ben_v20.957_45988']
#LANGUAGES=['kan_v81.355_114085']
#LANGUAGES=['kan_v92.164_58218']
#LANGUAGES=['kan_v111.786_42042']
#LANGUAGES=['kan_v111.149_57947']
#LANGUAGES=['kan_v81.183_126871']
#LANGUAGES=['exp1','exp10.279_20128','exp10.455_15269','exp10.476_15255','exp10.902_11593','exp11.064_11455'\
#          ,'exp11.218_10324'DoubleOcr'','exp11.552_8136','exp111.025_3160','exp123.612_2274','exp14.535_4746']

PSM=7
DYNAMIC_MARGINS = False
PERSPECTIVE_TRANSFORM = True

GOOGLE_OCR=True
TESS_OCR=False
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

#Preporcessing config
DOWLOAD_URL = "https://auth.anuvaad.org/download/"
# GV_OUTPUT_DIR ='/home/dhiraj/Documents/data/tess_training/batch_2/gv_json/*'
# OUTPUT_CSV_DIR = '/home/dhiraj/Documents/data/tess_training/batch_2/output/csv'
# OUTPUT_IMG_DIR  = '/home/dhiraj/Documents/data/tess_training/batch_2/output/images'

# GV_OUTPUT_DIR ='/home/dhiraj/Documents/data/tess_training/batch_2/gv_json/*'
# OUTPUT_CSV_DIR = '/home/dhiraj/Documents/data/tess_training/batch_2/output/csv'
# OUTPUT_IMG_DIR  = '/home/dhiraj/Documents/data/tess_training/batch_2/output/images'
GV_OUTPUT_DIR ='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/*.json'
OUTPUT_CSV_DIR = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/csv/'
OUTPUT_IMG_DIR  = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/images'

LINE_IMAGE_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark/tamil/benchmark_data/class1/*.png'
LINE_TEXT_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark/tamil/benchmark_data/class1/'
#GV_OUTPUT_DIR ='/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/batch_2/*'
#OUTPUT_CSV_DIR = '/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/csv'
#OUTPUT_IMG_DIR  = '/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/images'




##ERROR LINES AND CROPS FROM REPORT

error_directory='/home/ubuntu/tess_train_data_prep/reports/kannada_train/training_data_education_govt_orders_research/crops'
