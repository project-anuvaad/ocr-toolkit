import os
import sys
import glob
import config
import requests
import logging
import multiprocessing
from multiprocessing import Queue
from pdf_to_txt import TokenizePdf
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, filename=config.LOGS,
                    format='%(asctime)s-%(levelname)s-%(message)s')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

tokenization_queue = Queue()


def start_processes(workers=config.BATCH_SIZE):
    process = []
    for w in range(workers):
        process.append(multiprocessing.Process(target=tokenize_pdf))
        process[-1].start()


def tokenize_pdf():
    while True:
        try:
            TokenizePdf(tokenization_queue.get(block=True))
        except:
            pass
# def parse_files(parent_dir):
#     files = []
#     for child_dir in glob.glob(os.path.join(parent_dir,'*')):
#         child_dir_name = child_dir.split('/')[-1]
#         pdfs = glob.glob(os.path.join(child_dir,'*.pdf'))
#         if len(pdfs) < 2 :
#             logging.error('Parallel pdfs missing for file {} '.format(child_dir_name))
#         else :
#             files.extend(pdfs)

#     return files


def parse_files(parent_dir):
    return glob.glob(os.path.join(parent_dir))


def get_json_path(pdf_path):
    folder_name = pdf_path.split('/')[-2]
    pdf_name = pdf_path.split('/')[-1].split('.')[0]
    return os.path.join(config.OUTPUT_DIR, folder_name, '{}.json'.format(pdf_name))


def get_auth_token():
    try:
        res = requests.post(config.LOGIN, json={
                            "userName": config.USER, "password": config.PASS})
        auth_token = res.json()['data']['token']
        logging.info(" Authentication successful \n")
        return auth_token

    except Exception as e:
        logging.error('Error in authentication {}'.format(e), exc_info=True)
        return None


if __name__ == '__main__':

    auth_token = get_auth_token()

    if auth_token is not None:
        start_processes()
        files = parse_files(config.INPUT_DIR)
        # files.reverse()

        for pdf in tqdm(files, desc="Images"):
            try:
                if config.OVERWRITE:
                    tokenization_queue.put([pdf, auth_token])
                else:
                    json_path = get_json_path(pdf)
                    if not os.path.exists(json_path):
                        tokenization_queue.put([pdf, auth_token])
                    else:
                        print('{} already processed'.format(pdf))
            except Exception as e:
                logging.error('Error in processing PDF  {} due to {} {}'.format(
                    pdf, e), exc_info=True)

        print('All pdfs processed!')
