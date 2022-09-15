import cv2,glob
import pandas as pd
import json
import numpy as np
#import matplotlib.pyplot as plt
import config
import os
#import swifter

def get_crop_with_pers_transform(image, box, height=140):

    w = max(abs(box[0, 0] - box[1, 0]), abs(box[2, 0] - box[3, 0]))
    height = max(abs(box[0, 1] - box[3, 1]), abs(box[1, 1] - box[2, 1]))
    pts1 = np.float32(box)
    pts2 = np.float32(
        [[0, 0], [int(w), 0], [int(w), int(height)], [0, int(height)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result_img = cv2.warpPerspective(
        image, M, (int(w), int(height)))  # flags=cv2.INTER_NEAREST
    return result_img


def get_box(bbox):
    temp_box = []
    temp_box.append([bbox["boundingBox"]['vertices'][0]['x'],
                    bbox["boundingBox"]['vertices'][0]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][1]['x'],
                    bbox["boundingBox"]['vertices'][1]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][2]['x'],
                    bbox["boundingBox"]['vertices'][2]['y']])
    temp_box.append([bbox["boundingBox"]['vertices'][3]['x'],
                    bbox["boundingBox"]['vertices'][3]['y']])

    temp_box = np.array(temp_box)
    return temp_box

def validate_region(region):
    box = region['boundingBox']['vertices'] 

    #check for negative coords :
    for v in box:
        for coord in v:
            if v[coord] < 0 :
                return False
    #check for orientation:
    if box[0]['y'] >= box[2]['y'] or box[0]['x'] >= box[1]['x']:
        return False
    else :
        return True
def crop_region(coord,image,crop_name,crop_dir=None):
    try:
        c_x=0; c_y=0
        if validate_region(coord):
            vertices = coord['boundingBox']['vertices']
            if config.PERSPECTIVE_TRANSFORM:
                box = get_box(coord)
                box[0][0]=box[0][0]+c_x; box[0][1]=box[0][1]+c_y; box[1][0]=abs(box[1][0]-c_x); box[1][1]=box[1][1]+c_y
                box[2][0]=abs(box[2][0]-c_x); box[2][1]=abs(box[2][1]-c_y); box[3][0]=abs(box[3][0]+c_x); box[3][1]=abs(box[3][1]-c_y)
                crop_image = get_crop_with_pers_transform(image, box, height=abs(box[0,1]-box[2,1]))
            else :
                crop_image = image[vertices[0]['y']+c_y : abs(vertices[2]['y']-c_y) ,vertices[0]['x']+c_x : abs(vertices[2]['x']-c_x)]
            if config.CHECK:
                if crop_dir:
                    crop_path=os.path.join(crop_dir,crop_name)
                else:   
                    crop_path = os.path.join(config.OUTPUT_DIR + '/erro_crops_gt_google_vision', crop_name)
                cv2.imwrite(crop_path,crop_image)
            return crop_image
        else :
            print("Error in region   due to invalid coordinates", coord)
            return None
    except Exception as e:
        print("Error in region   due to invalid coordinates", e)
        return None

def write_to_file(file_path,text):
    
    with open(file_path, "w",encoding='utf8') as txtfile:
        txtfile.write("{}".format(text))

# def to_df(data_csv,folder,folder_name,prefix):     
#     data_df = pd.DataFrame(data_csv,columns=['path','boundingBox','key','score','g_conf','tess_text','ground_text'])    
#     data_df.to_csv(folder+"/" + prefix + '_' + folder_name + '.csv',index=False)

   
        
# def remove_trailing_space(a):
#     m_text = ''
#     for text in a.split(' '):
#         if len(text) > 0:
#             if m_text == '' :
#                 m_text += text
#             else :
#                 m_text = m_text + ' ' + text
#     return m_text


def cut_crops(row,image):
    gt_text = row['gt_text']
    coords  = json.loads(row['coord'].replace("'",'"'))
    crop_name = row['crop_name']
    write_to_file(os.path.join(config.error_directory,"erro_crops_gt_google_vision/")+crop_name.split(".png")[0]+".gt.txt",gt_text)
    crop_region(coords,image,crop_name,crop_dir=os.path.join(config.error_directory,"erro_crops_gt_google_vision"))
    

def cut_crops_form_df(df):

    pages  = df.groupby('image_name')
    for page in pages:
        image_name  = page[0]
        page_df     = page[1]
        print('Processing image ',image_name)
        image_path = os.path.join(config.IMAGE_DIR,"{}.png".format(image_name))
        image   = cv2.imread(image_path)          
        if len(page_df) > 0:
            page_df.apply(lambda x:cut_crops(x,image),axis=1)


def get_error_crops(eval_csv_path):

    eval_csv = pd.read_csv(eval_csv_path)
    correct_df = eval_csv[eval_csv['score']==1]
    error_df   = eval_csv[eval_csv['score'] < 1]

    #cut_crops_form_df(correct_df)
    cut_crops_form_df(error_df)

    #error_df.to_csv(os.path.join(config.error_directory, 'error_lines.csv'))
    #correct_df.to_csv(config.OUTPUT_DIR + '/correct_lines.csv')


         

if __name__ == '__main__':
    os.system('mkdir -p ' + os.path.join(config.error_directory,"erro_crops_gt_google_vision"))
    for eval_csv_path in glob.glob(config.OUTPUT_FILE):
        get_error_crops(eval_csv_path)