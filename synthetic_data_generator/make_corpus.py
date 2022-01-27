import os
from os import listdir
from os.path import isfile, join
import re
import random
from tqdm import tqdm
from config import num_lines
import config

filename=[]
s=[]
mypath=config.inptxt
listfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]

for txtfile in listfiles:
    with open(txtfile, 'r') as f:
        for lines in f:
            s.append(lines[:-1])
            
print("INPUT TXT FILES WITH TOTAL LINES: ",len(s))
def preprocess(lines):
    res=[]
    for line in tqdm(lines,desc="PREPROCESSING"):
        if len(line.split())>30:
            continue
        if len(line.split())<1:
            continue
        if len(line)<2:
            continue
        res.append(line)
    return res
            
def extract_single_word(lines,count):
    res=[]
    for line in lines:
        if len(line.split())==1:
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_english(lines,count):
    res=[]
    for line in lines:
        if re.search(r"[a-zA-z]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_numbers(lines,count):
    res=[]
    for line in lines:
        if re.search(r"[0-9]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_begin_numbers(lines,count):
    res=[]
    for line in lines:
        if re.search(r"^[0-9]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]

def extract_matra_mismatch_balanced(lines,symbols,count):
    res=[]
    a=count//len(symbols)
    for symbol in symbols:
        res.extend(extract_symbol(lines,symbol,a))
    random.shuffle(res)
    return res   
    
def extract_characters_mismatch(lines,symbols,count):
    res=[]
    for line in lines:
        if re.search(fr"[{symbols}]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_characters_mismatch_balanced(lines,symbols,count):
    res=[]
    a=count//len(symbols)
    for symbol in symbols:
        res.extend(extract_characters_mismatch(lines,symbol,a))
    random.shuffle(res)
    return res

def extract_dash(lines,count):
    res=[]
    for line in lines:
        if re.search("\w[-]\w",line):
            res.append(line)
        if re.search("\w [-] \w",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_full_stop(lines,count):
    res=[]
    for line in lines:
        #print(len(line))
        if line[-1]=="।":
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_roman(lines,count):
    res=[]
    for line in lines:
        if re.search(r"[ \[\(\-](?=[LXVI])(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})[ .\)\-]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_abbreviation_dot(lines,count):
    res=[]
    for line in lines:
        if re.search(r"[\u0900-\u0965][०]",line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_oc_symbol(lines,opening,closing,count):
    res=[]
    for line in lines:
        if re.search(fr'{opening}(.*){closing}',line):
            res.append(line)
    random.shuffle(res)
    return res[:count]

#### SYMBOLS
def extract_symbol(lines,symbol,count):
    res=[]
    for line in lines:
        if re.search(fr'[{symbol}]',line):
            res.append(line)
    random.shuffle(res)
    return res[:count]
def extract_symbols_balanced(lines,symbols,count):
    res=[]
    a=count//len(symbols)
    for symbol in symbols:
        res.extend(extract_symbol(lines,symbol,a))
    random.shuffle(res)
    return res

def extract_general(lines,count):
    random.shuffle(lines)
    return lines[:count]
    

def extract_corpus(lines,count):
    lines=preprocess(lines)
    res=[]
    print("AFTER PREPROCESS,LINES ",len(lines))
    tot=0
    spec_char_count=int(count*0.23)
    tot+=spec_char_count
    char_mis_count=int(count*0.10)
    tot+=char_mis_count
    matra_mis_count=int(count*0.20)
    tot+=matra_mis_count
    num_count=int(count*0.15)
    tot+=num_count
    english_count=int(count*0.08)
    tot+=english_count
    single_count=int(count*0.05)
    tot+=single_count
    rest_count=count-tot
    
    
    res.extend(extract_full_stop(lines,int(0.15*spec_char_count)))
    res.extend(extract_dash(lines,int(0.10*spec_char_count)))
    res.extend(extract_oc_symbol(lines,"\(","\)",int(0.10*spec_char_count)))
    res.extend(extract_oc_symbol(lines,'\"','\"',int(0.065*spec_char_count)))
    res.extend(extract_oc_symbol(lines,"\'","\'",int(0.035*spec_char_count)))
    res.extend(extract_roman(lines,int(0.15*spec_char_count)))
    res.extend(extract_abbreviation_dot(lines,int(0.10*spec_char_count)))
    res.extend(extract_symbols_balanced(lines,["\[","\{","\/","\;",\
                                               "\,","\.","\:","\!",\
                                               "\%","\<","\>","\?",\
                                               "\&","\#","\="],int(0.30*spec_char_count)))
    print("SPECIAL_CHAR_DONE")
    
    
    
    res.extend(extract_characters_mismatch_balanced(lines,["थ","ध","भ","म","ढ़","श्",\
                                                          "न्","प्","य","व","ब","इ"\
                                                          ,"ऐ","ण","र","ज़"],char_mis_count))
    
    print("CHAR_MISMATCH_DONE")
    
    
    res.extend(extract_matra_mismatch_balanced(lines,[str("आँ")[1],str("भू")[1],str("रं")[1],\
                                                      str("प्र")[1],str("र्क्रॉ")[5],str("सी")[1],\
                                                     str("सि")[1],str("खु")[1],str("न्हों")[4],\
                                                     str("के")[1],str("है")[1],str("तः")[1],\
                                                     str("पृ")[1]],matra_mis_count))
    
    print("MATRA_DONE")
    
    res.extend(extract_symbol(lines,str("है")[1],300))
    
    
    res.extend(extract_begin_numbers(lines,int(0.6*num_count)))
    res.extend(extract_numbers(lines,int(0.4*num_count)))
    
    
    res.extend(extract_english(lines,english_count))
    res.extend(extract_single_word(lines,single_count))
    
    
    res.extend(extract_general(lines,rest_count))
    print("DONE")
    
    random.shuffle(res)
    return res

r=extract_corpus(s,count=num_lines)
textfile = open(config.out_txt_file, "w")
for element in r:
    textfile.write(element + "\n")
textfile.close()

print("WRITTEN TO ",config.out_txt_file)