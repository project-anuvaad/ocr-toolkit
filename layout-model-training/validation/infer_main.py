
import layoutparser as lp
import cv2,os,glob,uuid
import numpy as np 
import config
from overlap_remove import RemoveOverlap
remove_overlap = RemoveOverlap()
image_paths =config.IMAGE_PATH
model_primalaynet = lp.Detectron2LayoutModel(config.YAML_PATH,model_path = config.MODEL_PATH,label_map = config.CLASS_MAPPING,extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.50] )

def update_box_format(coords,tags,score):
		final_coord =[]
		for idx,coord in enumerate(coords):
			temp_dict = {}; vert=[]
			temp_dict['identifier'] = str(uuid.uuid4())
			vert.append({'x':coord[0],'y':coord[1]})
			vert.append({'x':coord[2],'y':coord[1]})
			vert.append({'x':coord[2],'y':coord[3]})
			vert.append({'x':coord[0],'y':coord[3]})
			temp_dict['boundingBox']={}
			temp_dict['boundingBox']["vertices"] = vert
			final_coord.append(temp_dict)
		return final_coord
def draw_box(layout,image,name):
    font = cv2.FONT_HERSHEY_SIMPLEX 
    fontScale = 1; thickness =1;  region_color = (255, 0, 0) 
    bbox = []; tag =[];scores=[]
    for idx,ele in enumerate(layout):
        bbox.append(list(ele.coordinates))
        tag.append(ele.type)
        scores.append(format(ele.score,'.2f'))
    layouts  = update_box_format(bbox,tag,scores)
    regions =     remove_overlap.remove_overlap(layouts)
    for region in regions:
        image= cv2.rectangle(image, (int(region['boundingBox']['vertices'][0]['x']),int(region['boundingBox']['vertices'][0]['y'])), (int(region['boundingBox']['vertices'][2]['x']),int(region['boundingBox']['vertices'][2]['y'])), (255, 0, 0) , 5)

    cv2.imwrite(config.SAVE_PATH+str(name),image)
    return bbox,tag

def predict_primanet(image_paths,model_primalaynet):
	for image_path in glob.glob(image_paths):
		image  = cv2.imread(image_path)
		name = image_path.split("/")[-1]
		layout = model_primalaynet.detect(image)
		bbox,tag = draw_box(layout,image,name)
                
predict_primanet(image_paths,model_primalaynet)
