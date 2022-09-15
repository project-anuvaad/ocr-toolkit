# Ocr_benchmark for error profiling and tesseract training
 
### Anuvaad OCR Workflow output json to CSV file.
```
https://github.com/project-anuvaad/ocr-toolkit/tree/ocr_toolkit/ocr
```

In config.py
```
#Give the experiment name
EXP_NAME = 'GOOGLE_OCR_15_HINDI_GOOGLE' 

#Crop path to save respective images
CROP_PATH="/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/crops/hindi"

#GT_Source for CSV path
GT_SOURCE = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/csv/*.csv'

#Images to be saved path
IMAGE_DIR  = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/images'
IMAGE_FORMAT ='png'

#output path
OUTPUT_DIR = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json'

#Final output csv file for to be processed in errorprofiling
OUTPUT_FILE = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/ulca_report_hindi_benchmark_data_google_lines.csv'

#language as per tesseract model 
LANGUAGES=['Devanagari']


#json paths of the OCR flow and csv , images save directory
GV_OUTPUT_DIR ='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/*.json'
OUTPUT_CSV_DIR = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/csv/'
OUTPUT_IMG_DIR  = '/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/hindi_json/images'


#Error crops save directory
error_directory='/home/ubuntu/tess_train_data_prep/reports/kannada_train/training_data_education_govt_orders_research/crops'
```

```
step 1 : run preprocess_input_json.py (preprocess input jsons from ocr flow and download images and texts from anuvaad pipeline)
step 2 : run main.py ( makes a csv file with respect to google vision and tesseract and gives score for the text crops)
step 3 : run cut_lines.py (from downloaded images cut line crops using csv data generated and save)
```
