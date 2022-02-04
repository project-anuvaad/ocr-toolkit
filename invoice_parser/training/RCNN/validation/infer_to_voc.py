import layoutparser as lp
import cv2, os, glob, uuid
import numpy as np
import config
import os
from overlap_remove import RemoveOverlap

remove_overlap = RemoveOverlap()
image_paths = config.IMAGE_PATH
from pascal_voc_writer import Writer

model_primalaynet = lp.Detectron2LayoutModel(
    config.YAML_PATH,
    model_path=config.MODEL_PATH,
    label_map=config.CLASS_MAPPING,
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
)

# pip install pascal-voc-writer


def write_to_xml(layout, image, image_path, ouptput_dir):

    # Writer(path, width, height)
    writer = Writer(image_path, image.shape[1], image.shape[0])

    for idx, ele in enumerate(layout):
        xmin, ymin, xmax, ymax = list(ele.coordinates)
        tag = ele.type
        # scores = format(ele.score,'.2f')
        writer.addObject(tag, xmin, ymin, xmax, ymax)

    name = image_path.split("/")[-1][:-4]
    save_path = os.path.join(ouptput_dir, name + ".xml")
    print(save_path)
    writer.save(save_path)


def predict_primanet(image_paths, model_primalaynet, ouptput_dir):
    for image_path in glob.glob(image_paths):
        image = cv2.imread(image_path)

        layout = model_primalaynet.detect(image)
        write_to_xml(layout, image, image_path, ouptput_dir)


predict_primanet(image_paths, model_primalaynet, config.SAVE_PATH)
