from shapely.geometry import Polygon
from collections import Counter
from rtree import index
import copy
import numpy as np
#import src.utilities.app_context as app_context
import uuid, os, io, sys
#from src.services.horizontal_merging import horzontal_merging

class MapKeys:
    def __init__(self):
        self.left    =  None
        self.right   =  None
        self.top     =  None
        self.bottom  =  None

    def get_left(self,box):
        left = int(box['boundingBox']['vertices'][0]['x'])
        return left

    def get_right(self,box):
        right = int(box['boundingBox']['vertices'][1]['x'])

        return right

    def get_top(self,box):
        top = int(box['boundingBox']['vertices'][0]['y'])
        return top

    def get_bottom(self,box):
        bottom = int(box['boundingBox']['vertices'][3]['y'])
        return bottom
    def get_height(self,box):
        height = int(abs(self.get_top(box) - self.get_bottom(box)))
        return height
    def get_width(self,box):
        width =  int(abs(self.get_left(box) - self.get_right(box)))
        return width

keys = MapKeys()
class RemoveOverlap:
    def __init__(self):
        self.left    =  None
        self.right   =  None
        self.top     =  None
        self.bottom  =  None

    def update_coord(self,reg1,reg2):
        try:
            box1_top = keys.get_top(reg1); box1_bottom = keys.get_bottom(reg1)
            box1_left = keys.get_left(reg1); box1_right = keys.get_right(reg1)
            box2_top = keys.get_top(reg2); box2_bottom = keys.get_bottom(reg2)
            box2_left = keys.get_left(reg2); box2_right = keys.get_right(reg2)
            reg1["boundingBox"]["vertices"][0]['x']= min(box1_left,box2_left)
            reg1["boundingBox"]["vertices"][0]['y']= min(box1_top,box2_top)
            reg1["boundingBox"]["vertices"][1]['x']= max(box1_right,box2_right)
            reg1["boundingBox"]["vertices"][1]['y']= min(box1_top,box2_top)
            reg1["boundingBox"]["vertices"][2]['x']= max(box1_right,box2_right)
            reg1["boundingBox"]["vertices"][2]['y']= max(box1_bottom,box2_bottom)
            reg1["boundingBox"]["vertices"][3]['x']= min(box1_left,box2_left)
            reg1["boundingBox"]["vertices"][3]['y']= max(box1_bottom,box2_bottom)
        except:
            pass
        return reg1

    def get_polygon(self,region):
        points = []
        vertices = region['vertices']
        for point in vertices:
            points.append((point['x'], point['y']))
        if not (max(points)==(0,0) and min(points)==(0,0)):
            poly = Polygon(points)
            if not poly.is_valid:
                poly = poly.buffer(0.01)
            return poly
        else:
            return False
    def polygon_overlap(self,reg1,reg2,org_reg1,org_reg2):
        area1 = reg1.area
        area2 = reg2.area
        if area1>area2:
            if keys.get_left(org_reg1)<keys.get_left(org_reg2) and keys.get_right(org_reg1)>keys.get_right(org_reg2) \
                and keys.get_top(org_reg1)<keys.get_top(org_reg2) and keys.get_bottom(org_reg1)>keys.get_bottom(org_reg2) :
               return True
            if (reg2.intersection(reg1).area/area2)*100>50:
               return True
        if area1<area2:
            if keys.get_left(org_reg2)<keys.get_left(org_reg1) and keys.get_right(org_reg2)>keys.get_right(org_reg1) \
                and keys.get_top(org_reg2)<keys.get_top(org_reg1) and keys.get_bottom(org_reg2)>keys.get_bottom(org_reg1) :
               return True
            if (reg1.intersection(reg2).area/area1)*100>50:
               return True
        if reg1.contains(reg2) or reg2.contains(reg1):
               return True
        if (keys.get_top(org_reg2)<keys.get_top(org_reg1) and keys.get_bottom(org_reg2)>keys.get_bottom(org_reg1)) \
                and  (keys.get_top(org_reg2)>keys.get_top(org_reg1) and keys.get_bottom(org_reg2)<keys.get_bottom(org_reg1)):
               return True 
       
        return False
    
    def is_connected(self,region1, region2):
            
        region_poly = self.get_polygon(region2['boundingBox'])
        base_poly = self.get_polygon(region1['boundingBox'])
        area=0
        if region_poly and base_poly:
            total_intsc_area = base_poly.intersection(region_poly).area
            area1 = region_poly.area
            area2 = base_poly.area
            area = base_poly.intersection(region_poly)
            superimpose = self.polygon_overlap(region_poly,base_poly,region1,region2)
        if (superimpose) or (area and abs(keys.get_top(region1)-keys.get_top(region2))<keys.get_height(region2)*0.2) or (area and total_intsc_area>max(area1,area2)*0.3):
            return True
        else:
            return False

    def merge_overlap(self,text_regions):
        region_updated = []
        flag =False
        while len(text_regions)>0:
            check = False
            region_temp= text_regions[1:]
            for idx2,region2 in enumerate(region_temp):
                cond = self.is_connected(text_regions[0], region2)
                if cond:
                    region1 = self.update_coord(text_regions[0],region2)
                    text_regions[0] = copy.deepcopy(region1)
                    check =True ;  flag = True
                    del text_regions[idx2+1]
                    break    
            if check == False:
                region_updated.append(copy.deepcopy(text_regions[0]))
                del text_regions[0]
        return region_updated, flag

    def remove_overlap(self,layouts):
        flag=True
        while flag==True:
            layouts, flag = self.merge_overlap(layouts)
        return layouts
removeoverlap = RemoveOverlap()

def get_coord(bbox):
    temp_box_cv = []
    temp_box_cv.append(bbox["boundingBox"]['vertices'][0]['x'])
    temp_box_cv.append(bbox["boundingBox"]['vertices'][0]['y'])
    temp_box_cv.append(bbox["boundingBox"]['vertices'][2]['x'])
    temp_box_cv.append(bbox["boundingBox"]['vertices'][2]['y'])
    return temp_box_cv
