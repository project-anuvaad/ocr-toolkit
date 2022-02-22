from PIL import Image
import argparse
import cv2
import os
import re
import io
import config
import json


def find_and_remove_index(lis,ele,tmp_indx):
    if ele is not None:
        indx = lis.index(ele)
        del lis[indx]
    
    return lis
def find_index(lis,ele,tmp_indx):
    if ele is not None:
        indx = lis.index(ele)
        return indx
    return tmp_indx
def filter_dates(ids,eds):
    if ids is not None and eds is not None:
        if int(ids.split("/")[-1])>int(eds.split("/")[-1]):
            return eds,ids
        else:
            return ids,eds
    else:
        return ids,eds
    
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

    filetered_lines=[]
    for line in data:
        words=line.split()
        l = [w for w in words if re.match(r'[a-zA-Z0-9_.)-/(]*$', w, re.I)]

        filetered_line = " ".join(k for k in l if k != "/")
        filetered_lines.append(filetered_line)
    return filetered_lines

def check_pattern(pattern,lis,cls,prev_idx=None,content_check=None):
    tmp_lis = lis
    try:
        for idx,key in enumerate(lis):
            if cls in key:
                if content_check is not None:
                    l=[w for w in lis[idx+1:] if re.match(pattern, w) and content_check in w]
                else:
                    l=[w for w in lis[idx+1:] if re.match(pattern, w) and w not in classes]
                if len(l)>0:
                    idx  = find_index(lis,l[0],idx+1)
                if len(l)>0:  return idx,l[0]

        if prev_idx is not None:
            lis=lis[prev_idx+1:]

        if content_check is not None:
            l=[w for w in lis if re.match(pattern, w) and  content_check in w]

        else:
            l=[w for w in lis if re.match(pattern, w) and w not in classes]
        if len(l)>0:
            idx  = find_index(tmp_lis,l[0],prev_idx)
            return idx,l[0]
        return prev_idx,None
    except:
        return prev_idx,None

def set_index(current_index,prev_indx):
    if current_index is not None:
        return current_index
    else:
        return prev_indx
    
class PassportClass():
    
    def __init__(self,prev_idx,filetered_lines):
        self.prev_idx = prev_idx
        self.filetered_lines=filetered_lines
    
    
    def extract_passport_number(self,cls):
        
        self.prev_idx, val = check_pattern(r'[A-Za-z]{1}[0-9]{7}',self.filetered_lines,cls,prev_idx=None)
        return val
    def extract_candidate_name(self,cls):
        
        self.prev_idx, val = check_pattern(r'[A-Za-z]',self.filetered_lines,cls,prev_idx=self.prev_idx)
        return val

    def extract_surname(self,cls):
        self.prev_idx, val = check_pattern(r'[A-Za-z]',self.filetered_lines,cls,prev_idx=self.prev_idx)
        return val
    def extract_dob(self,cls):
        tmp_idx=self.prev_idx
        self.prev_idx, val = check_pattern(r'\d{2}\/\d{2}\/\d{4}',self.filetered_lines,cls)
        self.filetered_lines = find_and_remove_index(self.filetered_lines,val,tmp_idx)
        self.prev_idx = tmp_idx
        return val

    def extract_nationality(self,cls):
        content_check = "INDIAN"
        self.prev_idx, val = check_pattern(r'[A-Za-z]',self.filetered_lines,cls,prev_idx=self.prev_idx,content_check=content_check)
        return val

    def extract_gender(self,cls):
        for idx,key in enumerate(self.filetered_lines):
            if cls in key:
                l=[w for w in self.filetered_lines if w  in ["M","F","m","f"]]
                if len(l)>0:  return l[0]
        l=[w for w in self.filetered_lines if w  in ["M","F","m","f"]]
        if len(l)>0:
            return l[0]
        return None
    
    def extract_pob(self,cls):
        self.prev_idx, val = check_pattern(r'[A-Za-z]',self.filetered_lines,cls,self.prev_idx)
        return val

    def extract_doi(self,cls):
        self.prev_idx, val = check_pattern(r'\d{2}\/\d{2}\/\d{4}',self.filetered_lines,cls)
        self.filetered_lines = find_and_remove_index(self.filetered_lines,val,self.prev_idx)
        return val

    def extract_doe(self,cls):
        self.prev_idx, val = check_pattern(r'\d{2}\/\d{2}\/\d{4}',self.filetered_lines,cls)
        return val
        
        
def save_data(data,image_name):
    try:
        to_unicode = unicode
    except NameError:
        to_unicode = str
    output_file_name = config.OUTPUT_SAVE_DIR+image_name+".json"
    with io.open(output_file_name, 'w', encoding='utf-8') as outfile:
        str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    

def transform_data(lines,image_name):
    filetered_lines=clean_data(lines)
    #filetered_lines=lines
    pass_cls = PassportClass(prev_idx=0,filetered_lines=filetered_lines)
    passport = pass_cls.extract_passport_number("Passport No.")
    
    candidate_surname =pass_cls.extract_surname("Surname")
    candidate_name = pass_cls.extract_candidate_name("Given Name")
    candidate_nationality =pass_cls.extract_nationality("Nationality")
    candidate_dob =pass_cls.extract_dob("Date of Birth")
    candidate_gender =pass_cls.extract_gender("Sex")
    candidate_pob =pass_cls.extract_pob("Place of Birth")
    candidate_doi  =pass_cls.extract_doi("Date of Issue")
    candidate_doe =pass_cls.extract_doe("Date of Expiry")
    candidate_doi,candidate_doe= filter_dates(candidate_doi,candidate_doe)
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
    print("data",data)
    save_data(data,image_name)
    
    return [data]