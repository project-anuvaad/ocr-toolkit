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
import glob
import pandas as pd
from leven import levenshtein


def check_text_df(temp_df,image_crop):
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()
    if temp_df is None or len(temp_df)==0:
        temp_df = pytesseract.image_to_data(image_crop,config='--psm '+str(6), lang=config.EMPTY_DF_LANG  ,output_type=Output.DATAFRAME)
    
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()  
    if temp_df is not None and len(temp_df)==1:
        if 'text' in temp_df.keys() and isinstance(temp_df['text'][0], float):
            temp_df["text"] = temp_df.text.astype(str)
            text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=config.BASE_LANGUAGE)
            temp_df['text'][0] = text
        if 'text' in temp_df.keys() and temp_df['conf'][0]<config.DOUBLE_OCR_THRESHOLD:
            temp_df = pytesseract.image_to_data(image_crop,config='--psm 8', lang=config.EMPTY_DF_LANG,output_type=Output.DATAFRAME)
            temp_df = temp_df[temp_df.text.notnull()]
            temp_df = temp_df.reset_index()
            if temp_df is not None and len(temp_df)>0 and  isinstance(temp_df['text'][0], float):
                temp_df["text"] = temp_df.text.astype(str)
                text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=config.BASE_LANGUAGE)
                temp_df['text'][0] = text

    return temp_df


def check_text_df1(temp_df,image_crop):
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()
    if temp_df is None or len(temp_df)==0:
        temp_df = pytesseract.image_to_data(image_crop,config='--psm '+str(6), lang=config.TRAINED_EMPTY_DF_LANG  ,output_type=Output.DATAFRAME)
    
    temp_df = temp_df[temp_df.text.notnull()]
    temp_df = temp_df.reset_index()  
    if temp_df is not None and len(temp_df)==1:
        if 'text' in temp_df.keys() and isinstance(temp_df['text'][0], float):
            temp_df["text"] = temp_df.text.astype(str)
            text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=config.TRAINED_LANGUAGE)
            temp_df['text'][0] = text
        if 'text' in temp_df.keys() and temp_df['conf'][0]<config.DOUBLE_OCR_THRESHOLD:
            temp_df = pytesseract.image_to_data(image_crop,config='--psm 8', lang=config.TRAINED_EMPTY_DF_LANG,output_type=Output.DATAFRAME)
            temp_df = temp_df[temp_df.text.notnull()]
            temp_df = temp_df.reset_index()
            if temp_df is not None and len(temp_df)>0 and  isinstance(temp_df['text'][0], float):
                temp_df["text"] = temp_df.text.astype(str)
                text = pytesseract.image_to_string(image_crop,config='--psm 8', lang=config.TRAINED_LANGUAGE)
                temp_df['text'][0] = text

    return temp_df
        
        
def tesseract_original(image_crop):
    dfs = pytesseract.image_to_data(image_crop,config='--psm 6', lang=config.BASE_LANGUAGE  ,output_type=Output.DATAFRAME)
    dfs = check_text_df(dfs,image_crop)
    text,conf_dict  = process_dfs(dfs)
    return text,conf_dict

def tesseract_trained(image_crop):
    dfs = pytesseract.image_to_data(image_crop,config='--psm 6', lang=config.TRAINED_LANGUAGE  ,output_type=Output.DATAFRAME)
    dfs = check_text_df1(dfs,image_crop)
    text,conf_dict  = process_dfs(dfs)
    return text,conf_dict     

def process_dfs(temp_df):
#     print(temp_df)
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
def main():
    img_path = glob.glob(config.img_path)
    txt_path = config.txt_path
    save_csv_path = config.save_csv_path
    # print(len(img_path))
    groundTruth = []
    original = []
    trained = []
    scores = []
    images = []
    gt_lens = []
    mismatch_counts = []
    df = pd.DataFrame()
    for i, j in enumerate(img_path):
        filename = j.split("/")[-1].split(".png")[0]
        img_name = j.split("/")[-1]
        if os.path.exists(txt_path+filename+".gt.txt"):
            if config.TESS_OCR:
                j = cv2.imread(j)
                print("processing filename:",filename)
                file = open(txt_path+filename+".gt.txt","r")
                file = file.read()
                images.append(img_name)
                text,conf_dict = tesseract_original(j)
                original.append(text)
                text1,conf_dict1 = tesseract_trained(j)
                trained.append(text1)
                score, gt_len, mismatch_count = seq_matcher(str(text), str(text1))
                scores.append(score)
                gt_lens.append(gt_len)
                mismatch_counts.append(mismatch_count)
                groundTruth.append(file)

    df["groundTruth"] = groundTruth
    df['gt_text'] = original
    df['tess_text'] = trained
    df['score'] = scores
    df['gt_len'] = gt_lens
    df['mismatch_count'] = mismatch_counts
    df['crop_name'] = images
    df.to_csv(save_csv_path)

if __name__ == '__main__':
    main()