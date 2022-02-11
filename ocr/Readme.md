# Anuvaad OCR Process

Generating JSON or/and TXT from a pdf document containing  digitization information at line/word level with ANUVAAD WORKFLOW.


```bash
INPUT => PDF DOCUMENTS

PROVIDE parameters in ocr/config.py

COMPILE run.py to execute module.

OUTPUT => JSON OR/AND TXT FILE

PDF DOCS  => ANUVAAD SERVER => JSON FILE containing Digitized info of respective pdfs.

KEY PARAMETERS TO BE PROVIDED IN OCR/config.py

"""
INPUT DIR: Directory containing PDF Files to be digitized;
OUTPUT_DIR: JSON or/and txt output directory; 
LANGUAGE: Google vision lang; eg. hi
BATCH_SIZE: No. of Processes to be utilised; eg. 8
"""


"""
LOGS: Log File with path; eg. LOGS/mylog
SAVE_JSON: For JSON file output; bool value
SAVE_TXT: For Digitized Txt output; bool value
OVERWRITE: If already existing output, whether to overwrite; bool value
"""

#ANUVAAD LOGIN DETAILS AND WF SELECTION
#LOGIN DEV
LOGIN='https://auth.anuvaad.org/anuvaad/user-mgmt/v1/users/login'
USER="xyz@tarento.com"
PASS="xyzabc"

 
 
#ANUVAAD WORKFLOW CONFIG DEV
WF_INIT="https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/async/initiate"
WF_CODE  = "WF_A_FCWDLDBSOD15GVOTK"
SEARCH='https://auth.anuvaad.org/anuvaad-etl/wf-manager/v1/workflow/jobs/search/bulk'
DOWNLOAD="https://auth.anuvaad.org/download/"
UPLOAD='https://auth.anuvaad.org/anuvaad-api/file-uploader/v0/upload-file'

KEY FEATURES OF OCR MODULE

Multi-Processing for faster execution.
Anuvaad Digitization API is utilised for JSON/TXT generation.


PDFs to be processed are kept in a directory and directory path is provided in config INPUT_DIR flag.

In the Output Directory Path provided, This Pipeline will generate output files in output directory with a directory inside it with parent directory name of input pdfs.
JSON and txt file name will be the same as pdf name.

Eg: 
For   ../pdfs/*.pdf
INPUT_DIR=../pdfs/

Let OUTPUT_DIR=/home/xyz/

Then Pipeline will output /home/xyx/pdfs/*.json and /home/xyx/pdfs/*.txt

For Batch Size, Check with the number of cores available and Load at CPU.


Language flag is the flag list for the language of pdf. Following is mapping of language flag code with scripts: 
    "en" : ["Latin","eng"],
    "kn" : ['Kannada',"kan"],
    "gu": ["guj"],
    "or": ["ori"],
    "hi" : ["Devanagari","hin","eng"],
    "bn" : ["Bengali","ben"],
    "mr": ["Devanagari","hin","eng"],
    "ta": ['Tamil',"tam"],
    "te" : ["Telugu","tel"],
    "ml" :["Malayalam"],
    "ma" :["Marathi"]


In the SAVE_JSON flag, Put it True for JSON output for each PDF.
Likewise SAVE_TXT flag, Put it True for txt output to each pdf.
Both above can be simultaneously True for both json and txt output.


```
