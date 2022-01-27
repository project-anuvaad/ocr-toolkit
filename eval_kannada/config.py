

LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="dhiraj.daga@tarento.com"
PASS="Cv@123"





#Step 1 generate evaluation report

language = 'Kannada'
#language = 'tamPlus0.041_53588'
#language = 'tam_v4_1'
path = '/home/ubuntu/tess_train_data_prep/pdfs/kannada/training_data_good_judgment/'


#path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/data/'
#output_path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/result/'
#output_path_boxes= '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/test_word_boxes/'
#base_path = '/home/ubuntu/tesseract_evaluation_hindi/tesseract_evaluation/test_word_boxes/'




#output_path = '/home/ubuntu/tess_train_data_prep/reports/tamil/'
output_path = '/home/ubuntu/tess_train_data_prep/reports/kannada_train/'
output_path_boxes = output_path
base_path         = output_path


#Step 2 filter crops based on text score


score_threshold=1.0
tesserct_conf = 0.0
g_conf_threshold   = 0


eval_csv_path='/home/ubuntu/tess_train_data_prep/crops/tamil/benchmar_data_correction/average/*.csv'
crops_dir='/home/ubuntu/tess_train_data_prep/crops/tamil/benchmar_data_correction/'
data_csv_path = '/home/ubuntu/tess_train_data_prep/text_csv/tamil/'
