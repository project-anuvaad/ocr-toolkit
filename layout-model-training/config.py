IMAGE_PATH="./layout-model-training/validation/hindi_tamil_ocr_eval_pdf_images2/*.jpg"
MODEL_PATH="./layout-model-training/outputs/prima/mask_rcnn_R_50_FPN_3x/model_final.pth"
YAML_PATH="./layout-model-training/outputs/prima/mask_rcnn_R_50_FPN_3x/config.yaml"
SAVE_PATH="./layout-model-training/validation/hindi_tamil_ocr_eval_pdf_images2_result_post_process/"
CLASS_MAPPING={0:"LineRegion"}
RESUME=True
PRETRAINED_MODEL="./layout-model-training/outputs/prima/mask_rcnn_R_50_FPN_3x/pre_trained_model.pth"
