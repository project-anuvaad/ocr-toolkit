import os,glob
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
#listfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
listfiles = glob.glob(mypath)
for txtfile in listfiles:
    with open(txtfile, 'r') as f:
        for lines in f:
            s.append(lines[:-1])
            
print("INPUT TXT FILES WITH TOTAL LINES: ",len(s))
def preprocess(lines):
    res=[]
    for line in tqdm(lines,desc="PREPROCESSING"):
        if len(line.split())>12:
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
        if line[-1]==".":
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
    spec_char_count=int(count* 0.15)
    tot+=spec_char_count
    char_mis_count=int(count*0.20)
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
                                               "\&","\#","\=","\*","\@","\+"],int(0.30*spec_char_count)))
    print("SPECIAL_CHAR_DONE")
    
    
#KANNADA   
#     res.extend(extract_characters_mismatch_balanced(lines,["೦" ,"೧", "೨", "೩", "೪", "೫","೬","೭","೮","೯","ಕೆ", "೯","ಠ", "ಥ್ವಿ",  "ಶ್ರೀ","ಕ್ಕ", "ಖ್ಖ", "ಗ್ಗ", "ಘ್ಘ", "ಙ್ಙ","ಚ್ಚ", "ಛ್ಛ" ,"ಜ್ಜ" ,"ಝ್ಝ" ,"ಞ್ಞ","ಟ್ಟ" ,"ಠ್ಠ" ,"ಡ್ಡ", "ಢ್ಢ", "ಣ್ಣ" ,"ತ್ತ", "ಥ್ಥ", "ದ್ದ", "ಧ್ಧ" ,"ನ್ನ", "ಪ್ಪ", "ಫ್ಫ", "ಬ್ಬ" ,"ಭ್ಭ" ,"ಮ್ಮ", "ಯ್ಯ", "ರ್‍ರ" ,"ಲ್ಲ" ,"ವ್ವ" ,"ಶ್ಶ","ಷ್ಷ" ,"ಸ್ಸ", "ಹ್ಹ" ,"ಳ್ಳ","ಡ್ಜ್-"," ತ್ಮ", "ತ್ತೂ", "ಕ್ಷಿ","ಲ್ಕಿ" ,"ಲ್ಜಿ","ತ್ಮ","ಕ್ರಿ"],char_mis_count)) 
 
#MARATHI
#     res.extend(extract_characters_mismatch_balanced(lines,["०","१","२","३","४","५","६","७","८","९","अ","आ"," इ", "ई", "उ", "ऊ"," ए", "ऐ", "ओ", "औ", "अं", "अः","क", "ख", "ग"," घ", "ङ","च", "छ", "ज", "झ", "ञ","ट" ,"ठ" ,"ड" ,"ढ" ,"ण","त", "थ", "द", "ध", "न","प","फ","ब", "भ", "म","य"," र", "ल", "व", "श","ष"," स", "ह", "ळ", "क्ष", "ज्ञ","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
# ],char_mis_count))

#MALAYALAM
    res.extend(extract_characters_mismatch_balanced(lines,["അ","ആ","ഇ","ഈ","ഉ","ഊ","ഋ","ഌ","എ","ഏ","ഐ","ഒ","ഓ","ഔ","ക","ഖ","ഗ","ഘ","ങ","ച","ഛ","ജ","ഝ","ഞ","ട","ഠ","ഡ","ഢ","ണ","ത","ഥ","ദ","ധ","ന","ഩ","പ","ഫ","ബ","ഭ","മ","യ","ര","റ","ല","ള","ഴ","വ","ശ","ഷ","സ","ഹ","ഺ","൏","ൔ","ൕ","ൖ","൘","൙","൚","൛","൜","൝","൞","ൟ","ൠ","ൡ","൦","൧","൨","൩","൪","൫","൬","൭","൮","൯","൰","൱","൲","൳","൴","൵","൶","൷","൸","൹","ൺ","ൻ","ർ","ൽ","ൾ","ൿ","൰൧","൨൰","൨൰൧","൩൰","൱൰","൰൲൯൰൯","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
],char_mis_count))   
    
    print("CHAR_MISMATCH_DONE")
    
#KANNADA    
#     res.extend(extract_matra_mismatch_balanced(lines,[str("ಃ"),str("ಂ"),str("ೌ"),\
#                                                       str("ೋ"),str("ೊ"),str("ೈ"),\
#                                                      str("ೇ"),str("ೆ"),str("ೃ"),\
#                                                      str("ೂ"),str("ು"),str("ೀ"),\
#                                                      str("ಿ"),str("ಾ"),str("್"),str("–")],matra_mis_count))
#MARATHI    
#     res.extend(extract_matra_mismatch_balanced(lines,[str("ा"),str("ि"),str("ी"),\
#                                                       str("ु"),str("ू"),str("े"),\
#                                                      str("ै"),str("ो"),str("ौ"),\
#                                                      str("ं"),str("ः"),str("–"),\
#                                                       str("आँ"),str("भू"),str("रं"),\
#                                                       str("प्र"),str("र्क्रॉ"),str("सी"),\
#                                                      str("सि"),str("खु"),str("न्हों"),\
#                                                      str("के"),str("है"),str("तः"),\
#                                                      str("पृ")],matra_mis_count))

#MALAYALAM
    res.extend(extract_matra_mismatch_balanced(lines,[str("ഀ"),str("ഁ"),str("ം"),\
                                                      str("ഃ"),str("഻"),str("഼"),\
                                                     str("ാ"),str("ി"),str("ീ"),\
                                                     str("ഽ"),str("ു"),str("ൂ"),\
                                                      str("ൃ"),str("ൄ"),str("െ"),\
                                                      str("േ"),str("ൈ"),str("ൊ"),\
                                                     str("ോ"),str("ൌ"),str("്"),\
                                                     str("ൎ"),str("ൗ"),str("ൢ"),\
                                                     str("ൣ")],matra_mis_count))
    
    
    print("MATRA_DONE")
    
    #res.extend(extract_symbol(lines,str("है")[1],300))
    
    
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