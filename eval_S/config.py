
LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="dhiraj.daga@tarento.com"
PASS="Cv@123"





#Step 1 generate evaluation report

language = 'Devanagari'
#language  = 'hin_v4'
path = '/home/ubuntu/tess_train_data_prep/pdfs/to_process_S/'


#path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/data/'
#output_path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/result/'
#output_path_boxes= '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/test_word_boxes/'
#base_path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/test_word_boxes/'




output_path = '/home/ubuntu/tess_train_data_prep/reports/hi_good/'
output_path_boxes = output_path
base_path         = output_path


#Step 2 filter crops based on text score


score_threshold=1
tesserct_conf = 0.0
google_conf   = 0.0


# eval_csv_path='/home/ubuntu/tess_train_data_prep/reports/hi_good/good_hindi/gv.csv'
# crops_dir='/home/ubuntu/tess_train_data_prep/crops/hi_good'
# data_csv_path = '/home/ubuntu/tess_train_data_prep/text_csv/hi_good.csv'


#eval_csv_path='/home/ubuntu/tess_train_data_prep/reports/hindi/*/*.csv'
#crops_dir='/home/ubuntu/tess_train_data_prep/crops/hindi/hi_good'
#data_csv_path = '/home/ubuntu/tess_train_data_prep/text_csv/hindi/'


eval_csv_path='/home/ubuntu/tess_train_data_prep/reports/hi_good/avg_hindi_414_S_2/gv.csv'
crops_dir='/home/ubuntu/tess_train_data_prep/crops/eval_S/avg_S_2'
data_csv_path = '/home/ubuntu/tess_train_data_prep/text_csv/hindi/'
