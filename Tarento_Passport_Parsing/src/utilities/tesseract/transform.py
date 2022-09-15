from PIL import Image
import argparse
import cv2
import os
import re
import io
import config
import json

filter_patterns = ["\x0c", "\f", "\v", "\x0b", None, ""]
chars_to_remove = ['.', '|','!', '?','+','-',':',';','~']

   
classes =[
    "Passport No.",
    "Given Name(s)",
    "Surname",
    "Date of Birth",
    "Nationality",
    "Sex",
    "Place of Birth",
    "Date of Issue",
    "Date of Expiry"
    
]



def clean_data(data):

    filetered_regions=[]
    for idx,region in enumerate(data):
        lines = [
            line for line in region['text'].split("\n") if line not in filter_patterns
        ]
        lines = check_word(lines)  
        data[idx]['text'] = lines
         
    return data

def check_word(lines):
    try:
        clean_lines=[]
        for line in lines:
            line = ' '.join([c for c in line.split(" ") if c not in chars_to_remove])
            clean_lines.append(line)
        return clean_lines
    except:
        return lines

    
def check_lines(region):
    total_lines = len(region['text'])
    if total_lines==2:
        return region['text'][1]
    elif total_lines==1:
        return region['text'][0]
    elif total_lines>2:
        return " ".join(text for text in region['text'][2:])
    else:
        return "None"
class PassportClass():
    
    def __init__(self,filetered_regions):
        self.filetered_regions=filetered_regions
    
    
    def extract_passport_number(self,region):
        val = check_lines(region)
        return val
        
    def extract_candidate_name(self,region):
        val = check_lines(region)
        return val

    def extract_surname(self,region):
        val = check_lines(region)
        return val

    def extract_dob(self,region):
        val = check_lines(region)
        return val

    def extract_nationality(self,region):
        val = check_lines(region)
        return val

    def extract_gender(self,region):
        val = check_lines(region)
        if (len(val)>1 and "M" in val) or  (len(val)>1 and "m" in val):
            return "M"
        if (len(val)>1 and "F" in val) or (len(val)>1 and "f" in val):
            return "F"
            
        return val
    
    def extract_pob(self,region):
        val = check_lines(region)
        return val

    def extract_doi(self,region):
        val = check_lines(region)
        return val


    def extract_doe(self,region):
        val = check_lines(region)
        return val
    def extract_poi(self,region):
        val = check_lines(region)
        return val

        
def save_data(data,image_name):
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    output_file_name = config.OUTPUT_SAVE_DIR+str(image_name)+".json"
    with io.open(output_file_name, 'w', encoding='utf-8') as outfile:
        str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    

def transform_data(regions,image_name):
    filetered_regions=clean_data(regions)
    pass_cls = PassportClass(filetered_regions=filetered_regions)
    passport=candidate_surname=candidate_name=candidate_nationality="None"
    candidate_dob=candidate_gender=candidate_pob=candidate_doi=candidate_doe=candidate_poi="None"
    for region in filetered_regions:
        region_cls = region['class']
        
        if region_cls=="pass":
            passport = pass_cls.extract_passport_number(region)
        if region_cls=="sn":
            candidate_surname =pass_cls.extract_surname(region)
        if region_cls=="name":
            candidate_name = pass_cls.extract_candidate_name(region)
        if region_cls=="nt":
            candidate_nationality =pass_cls.extract_nationality(region)
        if region_cls=="dob":
            candidate_dob =pass_cls.extract_dob(region)
        if region_cls=="sex":
            candidate_gender =pass_cls.extract_gender(region)
        if region_cls=="pob":
            candidate_pob =pass_cls.extract_pob(region)
        if region_cls=="doi":
            candidate_doi  =pass_cls.extract_doi(region)
        if region_cls=="doe":
            candidate_doe =pass_cls.extract_doe(region)
        if region_cls=="poi":
            candidate_poi =pass_cls.extract_poi(region)
    data = {}
    data["passport no."] = passport
    data['Surname'] = candidate_surname
    data['First Name'] = candidate_name
    data['Nationality'] = candidate_nationality
    data['Date of Birth'] = candidate_dob
    data['Place of Birth'] = candidate_pob
    data['Gender'] = candidate_gender
    data['Date of Expiry'] = candidate_doe
    data['Date of Issue'] = candidate_doi
    data['Place of Issue'] = candidate_poi
    save_data(data,image_name)
    
    return [data]