import numpy as np
import cv2
import glob
import os


source = "/home/dhiraj/ocr/Mestro/data/testing/training_v2/"
output_dir = "/home/dhiraj/ocr/Mestro/data/testing/training_v2/stiched2/"

to_stich = [ "24999", "29999",'34999']

image_dir = "/home/dhiraj/ocr/Mestro/data/testing/training_v2/9999/"

for image_path in glob.glob(image_dir + "/*"):
    im_name = image_path.split("/")[-1]
    ims = []
    for dir in to_stich:
        ims.append(cv2.imread(os.path.join(source, dir, im_name)))

    cv2.imwrite(os.path.join(output_dir, im_name), np.hstack(ims))
