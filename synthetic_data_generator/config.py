import os
from os import listdir
from os.path import isfile, join
import re


####### MAKE_CORPUS

#LINE_SOURCES
inptxt="/home/ubuntu/tess_train_data_prep/text_file_synthetic/telugu/*.txt"

num_lines=70000 # To generate dataset        
out_txt_file="/home/ubuntu/tess_train_data_prep/text_file_synthetic/telugu/final_corpus_curated_and_legal.txt"





########## DATA GENERATION
#PROCESS=58
#FILEPATH='/home/ubuntu/data-generator'
#OUTPATH='/home/ubuntu/data/ocr'
PROCESS=6
OUTPATH='/home/ubuntu/tess_train_data_prep/crops/syndata/telugu/curated_and_legal_generated_data/'
gentxt="/home/ubuntu/tess_train_data_prep/text_file_synthetic/telugu/final_corpus_curated_and_legal.txt"
lines=15


#FONT SIZES
font_sizes=[25]

#FONT COLOUR
font_colour=[(0,0,0)]

