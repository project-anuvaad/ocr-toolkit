import cv2
import config
from src.services.layout import detect_layout
from src.utils.util import load_json, Logger, logging
from src.utils.app_context import app_context
from src.utils.post_processing.map_template import layout_processor


@Logger(module_name="invoice_to_json", logtime=True)
def invoice_to_json(invoice_props):
    logging("Request : {}".format(invoice_props.file))

    supplier_id = invoice_props.get_supplier_id()

    if supplier_id in config.SUPPORTED_SUPPLIERS:

        Layouts, Aggregate, Validate = (
            layout_processor[supplier_id]["group"](),
            layout_processor[supplier_id]["agg"],
            layout_processor[supplier_id]["val"](),
        )

        all_layouts = []
        if config.DEBUG:
            Layouts.set_layouts(load_json(invoice_props.get_file_name())["data"])
            Layouts.extract_and_group_text(None, None)
            all_layouts = Layouts.get_layouts()
        else:
            page_paths = invoice_props.get_im_paths()
            logging("This invoice has {} pages".format(len(page_paths)))
            for page_index, page in enumerate(page_paths):
                app_context["log_perfix"] = page_index + 1
                image = cv2.imread(page)
                Layouts.set_layouts(
                    detect_layout(image, supplier_id, Layouts.class_mapping)
                )
                Layouts.extract_and_group_text(image, invoice_props.get_ocr_mode())
                all_layouts.extend(Layouts.get_layouts())
            if not config.troubleShoot:
                invoice_props.del_images()
            app_context["log_perfix"] = ""
        invoice_layouts = Aggregate(all_layouts, Layouts.skip_class)
        invoice_layouts.segment_layout_regions()
        invoice_layouts.meger_truncated_regions()
        tranfomed_layouts = invoice_layouts.transform()

        validation_rerport = Validate.check_keys(tranfomed_layouts)

        if "'vaild': False" in str(validation_rerport):
            logging("key validation failed")
            return {
                "code": 300,
                "data": tranfomed_layouts,
                "raw": all_layouts,
                "report": validation_rerport,
                "msg": "ouptput sturcture not valid",
            }

        else:
            logging("Key validation passed")
            return {
                "code": 200,
                "data": tranfomed_layouts,
                "msg": "invoice to json completed",
            }
    logging("supplier {} not supported".format(supplier_id))
    return {"code": 400, "msg": "supplier {} not supported".format(supplier_id)}
