import cv2
import os
import uuid
import glob
import config
import numpy as np
import pandas as pd
from utils.utils import read_json,download_file

class Page:
    def __init__(self,page):
        self.page  = page
        self.lines = []
        self.line_coords = []
        self.line_text   = []
        self.line_id     = []
        self.line_class=[]
    
    def get_page_coords(self):
        return {'boundingBox' : page['boundingBox']}
    
    def get_image(self):
#        print(page)
        page_path = self.page['path']
        page_path = page_path.split('upload')[1]
        nparr = np.frombuffer(download_file(page_path,f_type='image'), np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    def get_lines(self):
        
        if len(self.lines) > 0:
            return self.lines
        regions = page['regions']
        if len(regions) < 2 :
            return []
        for para in regions:
            if 'regions' in para.keys() and len(para['regions']) > 0:
                self.lines.extend(para['regions'])
    
    def get_line_coords_and_gt(self):
        if len(self.line_coords) == 0:
            self.get_lines()
            for line in self.lines:
                self.line_text.append(self.get_text(line))
                self.line_coords.append({'boundingBox' : line['boundingBox']})
                self.line_id.append(line['identifier'] + '.png')
                self.line_class.append(line['class'])
                
        return self.line_coords, self.line_text,self.line_id,self.line_class
    
    def get_text(self,line):
        text = ''
        if 'regions' in line.keys() and len(line['regions']) > 0:
                for word in line['regions']:
                    if word is not None and type(word) is dict and 'text' in word.keys():
                        text = text + ' ' + str(word['text'])
                if len(text)>0:
                    text = text[1:]
        return text
    def update_name(self,line_ids,file_name):
        if len(line_ids)>0:
            updated_line_ids=[]
            for line in line_ids:
                line_id2 = line.split('.png')[0]+str(file_name)+".png"
                updated_line_ids.append(line_id2)

        return updated_line_ids
    
    
        


if __name__ == '__main__':

    os.system('mkdir -p ' + config.OUTPUT_CSV_DIR)
    os.system('mkdir -p ' + config.OUTPUT_IMG_DIR)

    gv_paths = glob.glob(config.GV_OUTPUT_DIR)
 #   print(gv_paths)
    
    for gv_path in gv_paths:
        try:
            file_identifier  = str(uuid.uuid4())
            file_name = gv_path.split('/')[-1][:-5]
            pdf_data = read_json(gv_path)
 #       print(pdf_data)
            pages = pdf_data['outputs'][0]['pages']
  #      print('Processing file ',file_name)
            for page_index, page in enumerate(pages):
                page_properties = Page(page)
            #try:
                image            = page_properties.get_image()
                if image is not None:
                    page_dimesnions  = page_properties.get_page_coords()
                    line_coords,line_text,line_id,line_clss= page_properties.get_line_coords_and_gt()
                    line_id = page_properties.update_name(line_id,file_name)
                    page_df = pd.DataFrame({'coords':line_coords, 'groundTruth':line_text,'images':line_id,'class':line_clss})
                    page_df['page_coords']  = str(page_dimesnions)
                
                    csv_path   =  os.path.join(config.OUTPUT_CSV_DIR, '{}_{}_{}.csv'.format(page_index,file_identifier,file_name))
                    image_path =  os.path.join(config.OUTPUT_IMG_DIR, '{}_{}_{}.png'.format(page_index,file_identifier,file_name)) 
                
                    page_df.to_csv(csv_path,index=False)
                    cv2.imwrite(image_path,image)
        except:
#            os.remove(file_name)
            print(file_name)
            pass
