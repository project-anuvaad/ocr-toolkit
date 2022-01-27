import cv2, io
import config
import json
import statistics
import numpy as np
import requests
import csv,os,uuid
from os import path
import pytesseract
from pytesseract import Output
from leven import levenshtein
from utils.dynamic_adjustment import validate_region
from google.cloud import vision
from anuvaad_auditor.loghandler import log_exception


os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/ubuntu/anuvaad-f7a059c268e4_new.json'
client = vision.ImageAnnotatorClient()

def get_file_name(csv_path):
    # return csv_path.split('/')[-3]
    return csv_path.split('/')[-1][:-4]


def get_page_resolution(page_data):
    page_info = json.loads(page_data['page_coords'].iloc[0].replace("'", '"'))
    height = page_info['boundingBox']['vertices'][2]['y']
    width = page_info['boundingBox']['vertices'][1]['x']
    return height, width


def scale_coords(page_data, image_shape, page_resolution):
    page_data['coords'] = page_data['coords'].str.replace("'", '"')
    page_data['coords'] = page_data['coords'].apply(json.loads)
    coords = page_data['coords'].values
    scaled_coords = []
    x_ratio = image_shape[1]/page_resolution[1]
    y_ratio = image_shape[0]/page_resolution[0]
    #print('ratios  ',x_ratio,y_ratio, page_resolution,image_shape)
    for coord in coords:
        region = {'boundingBox': {'vertices': []}}
        for point in coord['boundingBox']['vertices']:
            region['boundingBox']['vertices'].append(
                {'x': int(point['x'] * x_ratio), 'y': int(point['y'] * y_ratio)})
        scaled_coords.append(region)
    return scaled_coords


def frequent_height(coords):
    text_height = []
    if len(coords) > 0:
        for box in coords:
            if box:
                text_height.append(abs(box['boundingBox']['vertices'][0]['y'] -box['boundingBox']['vertices'][3]['y'] ))
            
        if len(text_height)>0:
            return statistics.median(text_height)
        else:
            return 0
    else:
        return 0

def crop_region(coord,image,cls,crop_name=None):
    try:
        c_x = config.C_X; c_y=config.C_Y
        if cls=="CELL":
            c_x = 10; c_y=5
        if validate_region(coord):
            vertices = coord['boundingBox']['vertices']
            if config.PERSPECTIVE_TRANSFORM:
                box = get_box(coord)
                box[0][0]=box[0][0]+c_x; box[0][1]=box[0][1]+c_y; box[1][0]=abs(box[1][0]-c_x); box[1][1]=box[1][1]+c_y
                box[2][0]=abs(box[2][0]-c_x); box[2][1]=abs(box[2][1]-c_y); box[3][0]=abs(box[3][0]+c_x); box[3][1]=abs(box[3][1]-c_y)
                crop_image = get_crop_with_pers_transform(image, box, height=abs(box[0,1]-box[2,1]))
            else :
                crop_image = image[vertices[0]['y']+c_y : abs(vertices[2]['y']-c_y) ,vertices[0]['x']+c_x : abs(vertices[2]['x']-c_x)]
            if config.CHECK:
                if config.CROP_SAVE:
                    crop_path=path.join(config.CROP_PATH,crop_name)
                else:   
                    crop_path = path.join(config.OUTPUT_DIR + '/crops', crop_name)
                
                cv2.imwrite(crop_path,crop_image)
                crop_path = path.join(config.OUTPUT_DIR + '/crops', crop_name)
                cv2.imwrite(crop_path, crop_image)
            return crop_image
        else :
            print("Error in region   due to invalid coordinates", coord)
            return None
    except Exception as e:
        print("Error in region   due to invalid coordinates", e)
        return None

def get_document_bounds(img,crop_name):
    try:
        # img = cv2.imencode('.jpg', img)[1].tostring()
        # img_id = "/home/ubuntu/test/"+str(uuid.uuid4())+"_.jpg"
        # cv2.imwrite(img_id,img)

        img = cv2.imencode('.jpg', img)[1].tostring()
        image = vision.Image(content=img)
        # with io.open(img_id, 'rb') as image_file:
        #     content = image_file.read()
        # #print("image read",content)
        # image = vision.Image(content=content)
        #print("client read",image)
        response = client.document_text_detection(image=image)
        #print("respinse read",response)
        resp = response.full_text_annotation
        #print("full text read",resp)
        image_text = ""
        temp_dict1 ={"text":[],"conf":[]}
        for i,page in enumerate(resp.pages):
            for block in page.blocks:

                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        image_text = image_text + " " + word_text
                        temp_dict1["text"].append(word_text)
                        temp_dict1["conf"].append(word.confidence*100)

        return image_text,temp_dict1
    except Exception as e:
        print("ERROR IN GOOGLE VISION OCR::",e)
        return "",{"text":[],"conf":[]}
        
def check_text_df(temp_df,image_crop,lang, median_height,psm):
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()
    if temp_df is None or len(temp_df)==0:
        temp_df = pytesseract.image_to_data(image_crop,config='--psm '+str(psm), lang=config.EMPTY_DF_LANG  ,output_type=Output.DATAFRAME)
    
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()  
    if temp_df is not None and len(temp_df)==1:
        if 'text' in temp_df.keys() and isinstance(temp_df['text'][0], float):
            temp_df["text"] = temp_df.text.astype(str)
            text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=lang)
            temp_df['text'][0] = text
        if 'text' in temp_df.keys() and temp_df['conf'][0]<config.DOUBLE_OCR_THRESHOLD:
            temp_df = pytesseract.image_to_data(image_crop,config='--psm 8', lang=config.EMPTY_DF_LANG,output_type=Output.DATAFRAME)
            temp_df = temp_df[temp_df.text.notnull()]
            temp_df = temp_df.reset_index()
            if temp_df is not None and len(temp_df)>0 and  isinstance(temp_df['text'][0], float):
                temp_df["text"] = temp_df.text.astype(str)
                text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=lang)
                temp_df['text'][0] = text

    return temp_df
    
def get_tess_text(image_crop, lang, median_height,crop_name):
    
    crop_height = image_crop.shape[0]
    if config.GOOGLE_OCR:
        g_text,g_conf_dict = get_document_bounds(image_crop,crop_name)
        return g_text,g_conf_dict

    if config.TESS_OCR:    
        if crop_height > median_height * 1.5:

            # experiment with FALL_BACK_LANGUAGE as orignal and trained
            if config.FALL_BACK_LANGUAGE is not None:
                fall_back_lang = config.FALL_BACK_LANGUAGE
            else:
                fall_back_lang = lang
            dfs = pytesseract.image_to_data(image_crop,config='--psm 6', lang=fall_back_lang  ,output_type=Output.DATAFRAME)
            dfs = check_text_df(dfs,image_crop,lang, median_height,6)
            text,conf_dict  = process_dfs(dfs)
            return text,conf_dict       
        else:
            dfs = pytesseract.image_to_data(image_crop,config='--psm '+str(config.PSM), lang=lang,output_type=Output.DATAFRAME)
            dfs = check_text_df(dfs,image_crop,lang, median_height,config.PSM)
            text,conf_dict  = process_dfs(dfs)
            return text, conf_dict

def seq_matcher(tgt_text, gt_text):
    if tgt_text is not None and gt_text is not None:
        tgt_text = remove_space(tgt_text)
        gt_text = remove_space(gt_text)
        mismatch_count = levenshtein(tgt_text, gt_text)
        gt_len = len(gt_text)
        if gt_len > 0:
            score = 1 - mismatch_count/gt_len
            if score < 0:
                score = 0
            return score, gt_len, mismatch_count
    return 0, 0, 0


def append_to_file(file_path, line_stats):
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(line_stats)


def get_box(bbox):
    temp_box = []
    temp_box.append([bbox["boundingBox"]['vertices'][0]['x'],
                    bbox["boundingBox"]['vertices'][0]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][1]['x'],
                    bbox["boundingBox"]['vertices'][1]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][2]['x'],
                    bbox["boundingBox"]['vertices'][2]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][3]['x'],
                    bbox["boundingBox"]['vertices'][3]['y']])

    temp_box = np.array(temp_box)
    return temp_box


def get_crop_with_pers_transform(image, box, height=140):

    w = max(abs(box[0, 0] - box[1, 0]), abs(box[2, 0] - box[3, 0]))
    height = max(abs(box[0, 1] - box[3, 1]), abs(box[1, 1] - box[2, 1]))
    pts1 = np.float32(box)
    pts2 = np.float32(
        [[0, 0], [int(w), 0], [int(w), int(height)], [0, int(height)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result_img = cv2.warpPerspective(
        image, M, (int(w), int(height)))  # flags=cv2.INTER_NEAREST
    return result_img


def process_dfs(temp_df):
    temp_df = temp_df[temp_df.text.notnull()]
    text = ""
    conf = 0
    temp_dict1 = {"text": [], "conf": []}
    for index, row in temp_df.iterrows():
        #temp_dict2 = {}
        conf = conf + row["conf"]
        temp_dict1["text"].append(row['text'])
        temp_dict1["conf"].append(row['conf'])
        text = text + " " + str(row['text'])
        # temp_dict1.append(temp_dict2)
    return text, temp_dict1

def remove_space(a):
    return a.replace(" ", "")


def read_json(json_path):
    with open(json_path, 'r') as j_file:
        j_data = json.load(j_file)
    return j_data


def download_file(outputfile, f_type='json'):
    download_url = config.DOWLOAD_URL + outputfile
    res = requests.get(download_url)
    if f_type == 'json':
        return res.json()
    else:
        return res.content
