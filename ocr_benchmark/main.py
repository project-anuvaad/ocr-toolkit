import config
import multiprocessing
from multiprocessing import Queue
from utils.helper import tess_eval,add_lines_to_tess_queue,append_line,init_file
import os
from os import path
from utils.helper import tess_eval, add_lines_to_tess_queue, append_line, init_file,add_org_lines_to_tess_queue


tessract_queue = Queue()
file_writer_queue = Queue()


def start_tess_eval(workers=config.BATCH_SIZE):
    process = []
    for w in range(workers):
        process.append(multiprocessing.Process(target=tesseract_eval))
        process[-1].start()


def tesseract_eval():
    while True:
        try:
            line_stats = tess_eval(tessract_queue.get(block=True))
            file_writer_queue.put(line_stats)
        except Exception as e:
            config.logging.error(
                'Error in tesseract ocr due to {} '.format(e), exc_info=True)


def start_write_to_file():
    process = multiprocessing.Process(target=write_to_file)
    process.start()


def write_to_file():
    while True:
        append_line(file_writer_queue.get(block=True))


if __name__ == '__main__':
    os.system('mkdir -p ' + path.join(config.OUTPUT_DIR,'crops'))
#    start_tess_eval()
 #   start_write_to_file()
  #  start_tess_eval()
 #   start_write_to_file()
#    init_file()
    for lang in config.LANGUAGES:
        if config.LINE_IMAGE_OCR:
            add_org_lines_to_tess_queue(config.GT_SOURCE, tessract_queue, lang)
        else:
            add_lines_to_tess_queue(config.GT_SOURCE, tessract_queue, lang)
