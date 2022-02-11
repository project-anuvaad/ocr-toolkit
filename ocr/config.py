#IO
INPUT_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/pdfs/hindi/*.pdf'

OUTPUT_DIR='/home/ubuntu/tess_train_data_prep/ulca_benchmark_v2/reports/hindi/'

BATCH_SIZE= 2


LOGS='ocr_tok.log'
SAVE_JSON=True

OVERWRITE=False

#LOGIN DEV
LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="dhiraj.daga@tarento.com"
PASS="Cv@123"

#WF CONFIG DEV
WF_INIT= "https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
WF_CODE  = "WF_A_FCWDLDBSOD15GVOTK_S"
#WF_CODE   = 'WF_A_OD10GV'
SEARCH='https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
DOWNLOAD="https://auth.anuvaad.org/download/"
UPLOAD='https://auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file'

craft_word="False"
craft_line="False"
line_layout = "False"
