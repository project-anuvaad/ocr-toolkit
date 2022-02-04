import layoutparser as lp
import config
import yaml
from src.utils.util import Logger


global layout_models
layout_models = {}


@Logger(module_name="loding_layout_model", logtime=True)
def load_model(supplier_id, class_mapping):
    print("loading model for : ", supplier_id)

    with open(config.MODEL_PATH, "r") as stream:
        model_meta = yaml.safe_load(stream)

    layout_models[supplier_id] = lp.Detectron2LayoutModel(
        model_meta[supplier_id]["CONFIG"],
        model_path=model_meta[supplier_id]["MODEL_PATH"],
        label_map=class_mapping,
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    )


def transform_to_dict(layouts):

    raw_layouts = []
    for idx, ele in enumerate(layouts):
        raw_layouts.append(
            {
                "class": ele.type,
                "coords": list(ele.coordinates),
                "score": format(ele.score, ".2f"),
            }
        )

    return raw_layouts


@Logger(module_name="get_layout_predictions", logtime=True)
def detect_layout(image, supplier_id, class_mapping):

    if supplier_id not in layout_models.keys():
        load_model(supplier_id, class_mapping)

    layouts = layout_models[supplier_id].detect(image)

    return transform_to_dict(layouts)
