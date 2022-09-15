from anuvaad_auditor.loghandler import log_info
from anuvaad_auditor.loghandler import log_exception
from anuvaad_auditor.loghandler import log_debug
from src.utilities.request_parse import File
from src.services.ocr import TextExtraction
import config
from src.utilities.tilt_alignment import Orientation



def process_input(app_context):
    try:
        sentences = []
        errors = []
        exceptions = []
        file_properties = File(app_context.application_context)
        sr = file_properties.set_sr()
        for im_index in range(file_properties.get_images_len()):
            image = file_properties.get_image(im_index)
            
            image_name = file_properties.get_images_name(im_index)
            if config.ALIGN:
                image,angle = Orientation(image,file_properties).re_orient_east()

            image_sentences = TextExtraction(
                image,
                image_name,
                file_properties.get_coords(im_index),
                file_properties.get_lang(),
            ).get_sentences()

            if type(image_sentences) is not str:
                sentences.extend(image_sentences)
            else:
                sentences.append({"source": None})
                if "Exception" not in image_sentences:
                    errors.append({"im_indx": im_index, "error": image_sentences})
                elif file_properties.check_key():
                    exceptions.append(
                        {"im_indx": im_index, "exception": image_sentences}
                    )
                else:
                    exceptions.append("Developer access needed to view the exception")

        log_info(" Completed ocr process", None)
        return sentences, errors, exceptions, file_properties.get_config()

    except Exception as e:
        log_exception("Error occured during ocr", app_context.application_context, e)
        return None, None, None, None


def OCR(app_context):

    log_debug(
        "process starting  for request {}".format(app_context.application_context),
        app_context.application_context,
    )
    try:
        sentences, errors, exceptions, config = process_input(app_context)
        if sentences != None:
            response = {"output": sentences, "config": config}
            if len(errors) > 0 or len(exceptions) > 0:
                response["errors"] = errors
                response["exceptions"] = exceptions

            return response
        else:
            return {"output": sentences, "config": config}
    except Exception as e:
        log_exception("Error occured during  ocr  ", app_context.application_context, e)
        return {"output": None, "config": None}
