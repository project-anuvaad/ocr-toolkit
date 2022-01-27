import config


def post_process_ocr_text(image_crop,ocr_text,ocr_conf):
    
    if config.POST_PROCESSING_MODE == None :
        return ocr_text,ocr_conf

    if config.POST_PROCESSING_MODE == 'FixInts':
        return process_ints(ocr_text),ocr_conf


















def process_ints(text):
    try:
        if type(text) in [int, float]:
            if int(text)== text :
                return str(int(text))
            else:
                return str(text)
        else :
            return str(text)
    except Exception as e:
        print(e)
        return str(text)