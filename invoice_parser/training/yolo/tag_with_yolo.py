import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (
    LOGGER,
    check_file,
    check_img_size,
    check_imshow,
    check_requirements,
    colorstr,
    increment_path,
    non_max_suppression,
    print_args,
    scale_coords,
    strip_optimizer,
    xyxy2xywh,
)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

import config


def load_model(weights=config.WEIGHT_PATH, device=config.DEVICE):
    device = select_device(device)
    return DetectMultiBackend(weights, device=device, dnn=False)


model = load_model()


@torch.no_grad()
def detect(
    image_path, model=model, image_size=config.IMAGE_SIZE, s_device=config.DEVICE
):

    # Load model

    stride, names, pt, jit, onnx, engine = (
        model.stride,
        model.names,
        model.pt,
        model.jit,
        model.onnx,
        model.engine,
    )
    imgsz = check_img_size(image_size, s=stride)  # check image size

    # Dataloader
    device = select_device(s_device)
    dataset = LoadImages(image_path, img_size=imgsz, stride=stride, auto=pt)
    bs = 1  # batch_size

    # Run inference
    # model.warmup(imgsz=(1, 3, *imgsz), half=half)  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    output = []
    for path, im, im0s, vid_cap, s in dataset:
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        # im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=None)  # , visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        # pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        pred = non_max_suppression(pred, config.CONF_THRESHOLD, config.IOU_THRESHOLD)

        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # detections per image
            p, s, im0, frame = path, "", im0s, getattr(dataset, "frame", 0)
            p = Path(p)  # to Path

            s += "%gx%g " % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    bbox = {"vertices": []}

                    bbox["vertices"].append({"x": int(xyxy[0]), "y": int(xyxy[1])})
                    bbox["vertices"].append({"x": int(xyxy[2]), "y": int(xyxy[1])})
                    bbox["vertices"].append({"x": int(xyxy[2]), "y": int(xyxy[3])})
                    bbox["vertices"].append({"x": int(xyxy[0]), "y": int(xyxy[3])})

                    output.append(
                        {
                            "class": names[int(cls)],
                            "boundingBox": bbox,
                            "conf": round(float(conf), 2),
                        }
                    )
    return output
