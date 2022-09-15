import cv2
import os
import uuid
import glob
import config
import numpy as np
import pandas as pd

if __name__ == '__main__':

    os.system('mkdir -p ' + config.OUTPUT_CSV_DIR)

    lines = glob.glob(config.LINE_IMAGE_DIR)
    #try:

    page_df = pd.DataFrame(columns=['coords', 'groundTruth','images','class'])
    line_coords=[];  line_texts=[] ;   line_ids=[];  line_clsses=[]
    for line_index, line in enumerate(lines):
        
        line_identifier  = str(uuid.uuid4())
        image            = cv2.imread(line)
        image_id         = line.split("/")[-1].split(".")[0]
        if image is not None:
            line_coord = "None";  line_id= str(line)
            line_clss = "LINE_IMAGE"
            line_obj = open(config.LINE_TEXT_DIR+str(image_id)+".gt.txt","r")
            line_text = line_obj.read()
            line_coords.append(line_coord)
            line_texts.append(line_text)
            line_ids.append(line_id)
            line_clsses.append(line_clss)
    page_df['coords'] =  line_coords;  page_df['groundTruth'] =  line_texts
    page_df['images'] =  line_ids;  page_df['class'] =  line_clsses
    csv_path   =  os.path.join(config.OUTPUT_CSV_DIR, '{}.csv'.format(lines[0].split("/")[-2]))
    #image_path =  os.path.join(config.OUTPUT_IMG_DIR, '{}_{}_{}.png'.format(file_name,page_index,file_identifier)) 

    page_df.to_csv(csv_path,index=False)
    #print(page_df)
#     except:
# #            os.remove(file_name)
#         pass
