import os
import config
from src.utils.util import pdf_to_im_path, Logger


class Invoice:
    def __init__(self, file):
        self.file = file
        self.im_paths = None
        self.conf = None

    @Logger(module_name="get_supplier")
    def get_supplier_id(self):
        return self.file["supplierId"]

    def get_file_name(self):
        return self.file["invoice"][:-4]

    @Logger(module_name="pdf_to_image", logtime=True)
    def get_im_paths(self):

        pdf_path = os.path.join(config.BASE_DIR, "input", self.file["invoice"])
        self.im_paths = pdf_to_im_path(pdf_path, config.EXRACTION_RESOLUTION)
        return self.im_paths

    def del_images(self):
        for im in self.im_paths:
            os.system('rm "{}"'.format(im))

    def set_config(self, conf):
        self.conf = conf

    def get_ocr_mode(self):
        if "ocr" in self.conf.keys():
            return self.conf["ocr"]
        return None

    def set_job_id(self, job_id):
        self.file["jobId"] = job_id
