#IO
#INPUT_DIR='/home/srihari/Desktop/anuvaad-toolkit/t3'
#OUTPUT_DIR='/home/srihari/Desktop/anuvaad-toolkit/outputs'

#INPUT_DIR='/home/dhiraj/Documents/benchmark/t1'
#OUTPUT_DIR='/home/dhiraj/Documents/benchmark/t1'

#INPUT_DIR='/home/dhiraj/Documents/Anuwad/AIB/ta_set_1'
#OUTPUT_DIR='/home/dhiraj/Documents/Anuwad/AIB/ta_set_1'

#<<<<<<< HEAD
#INPUT_DIR  = '/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/playground/to_process'
#OUTPUT_DIR = '/home/ubuntu/tess_train_data_prep/reports/hindi/batch_2/playground/'
#=======
#INPUT_DIR  = '/home/ubuntu/tess_train_data_prep/pdfs/tamil/final_eval_pdfs/*.pdf'
#OUTPUT_DIR = '/home/ubuntu/tess_train_data_prep/reports/eval_tamil/eval_tamil_data_reports_v2_craft_lines'
#>>>>>>> 16a636c6bb4c02c6082afba90db1103b2096063b
INPUT_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/pdfs/hindi/*.pdf'
#OUTPUT_DIR='/home/ubuntu/tess_train_data_prep/reports/hindi/eval_hindi_data_reports_v2_layout_lines'
OUTPUT_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/'

BATCH_SIZE= 3


LOGS='ocr_tok.log'
SAVE_JSON=True



OVERWRITE=False

#LOGIN DEV
LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="dhiraj.daga@tarento.com"
PASS="Cv@123"

#LOGIN STAGE
# LOGIN='https://stage-auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
# USER="stageuser@tarento.com"
# PASS="Welcome@123"


#WF CONFIG DEV
WF_INIT= "https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
WF_CODE  = "WF_A_FCWDLDBSOD15GVOTK"
#WF_CODE   = 'WF_A_OD10GV'
SEARCH='https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
DOWNLOAD="https://auth.anuvaad.org/download/"
UPLOAD='https://auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file'

#WF CONFIG STAGE
# WF_INIT= "https://stage-auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
# WF_CODE  = "WF_A_FCWDLDBSOD15GVOTK"
# SEARCH='https://stage-auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
# DOWNLOAD="https://stage-auth.anuvaad.org/download/"
# UPLOAD='https://stage-auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file'
craft_word="False"
craft_line="False"
line_layout = "False"
