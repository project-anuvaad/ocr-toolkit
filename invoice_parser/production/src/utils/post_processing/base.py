import pytesseract
from pytesseract import Output
from src.utils.util import crop_im
import config
import copy
import os
from multiprocessing import Pool
from src.utils.util import Logger


class LayoutBase:
    def __init__(self):
        self.layouts = []
        self.score = 0
        self.classs = None
        self.corp_config = {}
        self.lang = None
        self.skip_class = []
        self.tabular_class = []
        self.class_mapping = {}
        self.ocr_mode = None

    def process(self, c_ls, text):
        default = None
        return getattr(self, "process_" + str(c_ls), lambda: default)(text)

    def set_layouts(self, layouts):
        self.layouts = layouts

    def get_layouts(self):
        return self.layouts

    def get_crop_config(self, cls):
        if cls in self.crop_config.keys():
            return self.crop_config[cls]
        return None

    def ocr(self, box):
        if box["class"] not in self.skip_class:

            if "text" not in box.keys():
                crop = crop_im(
                    self.image, box["coords"], self.get_crop_config(box["class"])
                )
                if box["class"] in self.tabular_class:
                    if self.ocr_mode == "ACCURATE":
                        box["text"] = pytesseract.image_to_data(
                            crop,
                            lang=self.lang,
                            config="--psm 6",
                            output_type=Output.DICT,
                        )
                    else:
                        box["text"] = pytesseract.image_to_data(
                            crop, lang=self.lang, output_type=Output.DICT
                        )

                else:
                    box["text"] = pytesseract.image_to_string(crop, lang=self.lang)
        return box

    @Logger(module_name="get_text", logtime=True)
    def get_text(self, image, ocr_mode):
        self.image = image
        self.ocr_mode = ocr_mode
        if config.MULTI_OCR:

            workers = int(os.cpu_count() / 4)
            if workers == 0:
                workers = 1
            pool = Pool(workers)
            self.layouts = pool.map(self.ocr, self.layouts)
        else:
            for box_index, box in enumerate(self.layouts):
                self.layouts[box_index] = self.ocr(box)

    @Logger(module_name="get_and_group_text", logtime=True)
    def extract_and_group_text(self, image, ocr_mode):
        if not config.DEBUG:
            self.layouts.sort(key=lambda y: y["coords"][1])
            self.get_text(image, ocr_mode)
        for box_index, box in enumerate(self.layouts):
            crop_cls = box["class"]
            self.score = float(box["score"])
            self.classs = crop_cls
            if crop_cls not in self.skip_class:

                processed_layout = self.process(
                    crop_cls, self.layouts[box_index]["text"]
                )
                if processed_layout != None:
                    # To rectify a case of mis-calssification by layout model
                    if "class" in processed_layout.keys():
                        self.layouts[box_index]["data"] = processed_layout["data"]
                        self.layouts[box_index]["class"] = processed_layout["class"]
                    else:
                        self.layouts[box_index]["data"] = processed_layout
                else:
                    pass

    def save_layouts(self, path):
        with open(path, "w") as output_file:
            output_file.write(self.layouts)


class AggregateBase:
    def __init__(self, layouts, skip_class):
        self.layouts = layouts
        self.skip_class = skip_class
        self.layout_segments = None

    def segment_layout_regions(self):
        pass

    @Logger(module_name="merge_across_pages", logtime=True)
    def meger_truncated_regions(self):
        for index, segment in enumerate(self.layout_segments):
            self.layout_segments[index] = copy.deepcopy(self.merge(segment))

    def merge(self, segment):
        return segment

    def transform(self):
        pass


class ValidateBase:
    def validate_keys(self, keys, respose):
        valid = True
        failed_for = None
        for key in keys:
            if key in respose.keys() and respose[key] != None:
                pass
            else:
                valid = False
                failed_for = key
                break
        return {"vaild": valid, "failed_for": failed_for}
