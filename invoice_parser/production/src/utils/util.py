import re
import os
import json
import config
import uuid
import pdf2image
import datetime
import time
from src.utils.app_context import app_context


def find_pattern_index(lis, pattern, last=False, index=True, all=False):
    # returns the first occurance of a given pattern
    try:
        element = 0
        if last:
            element = -1
        if index:
            return lis.index([i for i in lis if re.findall(pattern, i)][element])
        elif all:
            return [i for i in lis if re.findall(pattern, i)]
        return [i for i in lis if re.findall(pattern, i)][element]

    except Exception as e:
        print("Error in finding pattern", e)
        return None


def pdf_to_im_path(pdf_path, dpi):

    image_filename = (
        pdf_path.split("/")[-1][:-4]
        .replace(" ", "")
        .replace("(", "_")
        .replace(")", "_")
    )

    working_dir = os.path.join(
        config.BASE_DIR,
        "output",
        "images",
        str(uuid.uuid4()),
        image_filename,
    )
    os.system("mkdir -p {}".format(working_dir))

    return pdf2image.convert_from_path(
        pdf_path,
        dpi=dpi,
        output_file=image_filename,
        output_folder=working_dir,
        fmt="jpg",
        paths_only=True,
    )


def crop_im(im, coord, margin=None):
    xmin, ymin, xmax, ymax = coord
    if margin is None:
        crop = im[int(ymin) : int(ymax), int(xmin) : int(xmax)]
    else:
        crop = im[
            int(ymin - margin["y"]) : int(ymax + margin["y"]),
            int(xmin - margin["x"]) : int(xmax + margin["x"]),
        ]

    return crop


def sort_regions(text_df, sorted_text, line_id):

    line_id += 1
    check_y = text_df.iloc[0]["top"]
    spacing_threshold = text_df.iloc[0]["height"] * 0.5

    same_line = text_df[abs(text_df["top"] - check_y) < spacing_threshold]
    next_lines = text_df[abs(text_df["top"] - check_y) >= spacing_threshold]

    sort_lines = same_line.sort_values(by=["left"])
    sort_lines["id"] = line_id
    sorted_text.append(sort_lines)
    if len(next_lines) > 0:
        sort_regions(next_lines, sorted_text, line_id)

    return sorted_text


def load_json(pdf_name):
    json_name = pdf_name + ".json"
    json_path = os.path.join(config.INTM_OUTPUT_PATH, json_name)
    with open(json_path) as jp:
        data = json.load(jp)
    return data


def create_ouput_dirs(job_id):

    output_dir = os.path.join(config.BASE_DIR, "output", "service_output", job_id)

    fine = os.path.join(output_dir, "fine")
    run_time_errors = os.path.join(output_dir, "run_time_error")
    validation_errors = os.path.join(output_dir, "validation_error")
    for dir in [fine, run_time_errors, validation_errors]:
        os.system("mkdir -p {}".format(dir))
    return fine, run_time_errors, validation_errors, output_dir


def logging(msg):
    log_prefix = app_context["log_perfix"]
    if log_prefix != "":
        log = "{} : For page {} {} \n".format(
            str(datetime.datetime.now())[:19], log_prefix, msg
        )
    else:
        log = "{} : {} \n".format(str(datetime.datetime.now())[:19], msg)
    print(log)
    with open(config.LOGS, "a") as log_file:
        log_file.write(log)


class Logger:
    def __init__(
        self, module_name=None, troubleShoot=config.troubleShoot, logtime=False
    ):
        self.module_name = module_name
        self.troubleShoot = troubleShoot
        self.logtime = logtime

    def __call__(self, func):
        def logs(*args, **kwargs):
            if self.troubleShoot:
                result = func(*args, **kwargs)
                return result
            else:
                try:
                    if self.logtime:
                        start_time = time.time()
                    logging("Started : {}".format(self.module_name))

                    result = func(*args, **kwargs)
                    if self.logtime:
                        time_taken = time.time() - start_time
                        logging(
                            "Time taken for  : {} is {}".format(
                                self.module_name, round(time_taken, 3)
                            )
                        )

                    return result
                except Exception as e:
                    logging(
                        "Error in processin {} due to {} \n".format(self.module_name, e)
                    )
                    return {"code": 500}

        return logs


@Logger(module_name="save_response_to_disk")
def save_json(json_dir, data, pdf_name):
    if ".pdf" in pdf_name:
        json_path = os.path.join(json_dir, pdf_name[:-4] + ".json")
    else:
        json_path = os.path.join(json_dir, pdf_name + ".json")
    with open(json_path, "w", encoding="utf8") as write_file:
        json.dump(data, write_file, ensure_ascii=False)
