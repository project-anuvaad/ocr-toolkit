import os
from os import listdir
from os.path import isfile, join
import re


####### MAKE_CORPUS

#LINE_SOURCES
inptxt="line_txt/"

num_lines=40000 # To generate dataset        
out_txt_file="outcorpus.txt"





########## DATA GENERATION
#PROCESS=58
#FILEPATH='/home/ubuntu/data-generator'
#OUTPATH='/home/ubuntu/data/ocr'
PROCESS=2
OUTPATH='../crops/syndata/hindi/set1/'
gentxt="outcorpus.txt"



#FONT SIZES
font_sizes=[25]

#FONT COLOUR
font_colour=[(0,0,0)]

