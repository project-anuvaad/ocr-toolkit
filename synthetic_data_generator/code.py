import numpy as np
import random
from PIL import ImageFont, ImageDraw, Image
from os import listdir
from os.path import isfile, join
import string
import uuid
import json
from config import OUTPATH
import config


def file_list(mypath):
    onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles


def create_image(background,font,symbol,font_size,col,path):
    image = Image.open(background)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    #image=image.resize((200,200))
    font_pil = ImageFont.truetype(font, font_size)
    ascent, descent = font_pil.getmetrics()  
    try:
        if symbol==" ":
            a=font_pil.getmask('-').getbbox()[2]
        else:
            a=font_pil.getmask(symbol).getbbox()[2]
    except TypeError:
        print("TYPEERROR handled due to",symbol)
        #a=font_pil.getmask('M').getbbox()[2]
        return None
    text_width = a
    text_height = ascent+descent
    text_width+=int(0.03*(text_width))
    text_height+=int((0.10*text_height))
    image=image.resize((text_width+8,text_height),Image.ANTIALIAS)
    a=text_width//2
    b=ascent+int(0.05*(ascent))
    #image=image.crop((2,2,20+text_width,20+text_height))
    draw=ImageDraw.Draw(image)
    draw.text((8,text_height//2),symbol,col,font=font_pil,anchor="lm")
    #image.thumbnail([100,100], Image.ANTIALIAS)
    image_id=str(uuid.uuid4())
    image.save(join(config.OUTPATH,image_id)+'.png')
    with open(join(config.OUTPATH,image_id)+".gt.txt", 'w') as f:
        f.write(symbol)
    return image

def generator():
    bgs=file_list('BG_PAPER/')
    font_pack=file_list('font_files/')
    #font_colour=[(0,0,0),(25,25,25),(65,65,65)]
    #font_sizes=range(15,116,10)
    #font_sizes=[35,55,75,95,115]   ###range(15,116,10)
    #symbols=list(string.printable[:94])
    #symbols.append(u"\u00A9")
    #symbols.append(u"\u2122")
    #symbols.append(" ")
    symbols=[]
    with open(config.gentxt, 'r') as f:
        for lines in f:
            symbols.append(lines[:-1])
    font_colour=config.font_colour
    font_sizes=config.font_sizes
    for col in font_colour:
        for font_size in font_sizes:
            for background in bgs:
                font_idx =0
                for idx,symbol in enumerate(symbols):
                    #for font_idx,font in enumerate(font_pack):
                    if font_idx<len(font_pack):
                        font = font_pack[font_idx]
                        font_idx+=1
                    else:
                        font_idx=0
                        font = font_pack[font_idx]
                        font_idx+=1
                    yield background,font,symbol,font_size,col
        #print("Percent Completed : ",((k+1)/len(font_pack))*100)  

