import datetime
import uuid
import os


API_URL_PREFIX = "/mestro"
HOST = "0.0.0.0"
PORT = 5000

SUPPORTED_SUPPLIERS = ["SkellefteaKraft"]

MODEL_PATH = "./src/utils/layout/models.yaml"

MULTI_OCR = True
OCR_MODE = "FAST"  # ['FAST',"ACCURATE"]

EXRACTION_RESOLUTION = 300
BASE_DIR = "./base_dir"
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOGS = "{}/{}_{}.logs".format(LOGS_DIR, str(datetime.datetime.now())[:10], uuid.uuid4())
os.system("mkdir - p {}".format(LOGS_DIR))


# DEV TOOLS
troubleShoot = False
DEBUG = False
SAVE = True
INTM_OUTPUT_PATH = ""
