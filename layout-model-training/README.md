# Scripts for training Layout Detection Models using Detectron2


## Usage
- It is used for training layout detection like Paragraph,Header,Footer,Image,Table,Cell and Maths formula.
- We can define new layout class according to use case.


## module

- In `tools/`, we provide a series of handy scripts for converting data formats and training the models.
- In `scripts/`, it lists specific command for running the code for processing the given dataset. 
- The `configs/` contains the configuration for different deep learning models, and is organized by datasets.
- In `voc2coco/` convert pascal voc format to coco format and split coco dataset into training and validation.
- In `validation/` validation of test data with layout bounding box. 

##  Datasets
- Prima Layout Analysis Dataset [`scripts/train_prima.sh`](https://github.com/Layout-Parser/layout-model-training/blob/master/scripts/train_prima.sh)
    - You will need to download the dataset from the [official website](https://www.primaresearch.org/dataset/) and put it in the `data/prima` folder. 
    - As the original dataset is stored in the [PAGE format](https://www.primaresearch.org/tools/PAGEViewer), the script will use [`tools/convert_prima_to_coco.py`](https://github.com/Layout-Parser/layout-model-training/blob/master/tools/convert_prima_to_coco.py) to convert it to COCO format. 
- Judgements and Ncert books dataset
- Synthetically generated datset
- Layout classes: Paragraph,Header,Footer,Image,Table,Cell and Maths formula 

- The final dataset folder structure should look like:
    ```bash
    data/
    └── prima/
        ├── Images/
        ├── XML/
        ├── License.txt
        └── annotations*.json
    ```

## convert pascal to coco format
This is script for converting VOC format XMLs to COCO format json.

How to use
1. Make labels.txt
    - labels.txt if need for making dictionary for converting label to id.

Sample labels.txt

    Label1
    Label2
...
2. Run script

    2.1 Usage 1(Use annotation paths list)
    Sample paths.txt

    /path/to/annotation/file.xml
    /path/to/annotation/file2.xml
...
```bash
$ python voc2coco.py \
    --ann_paths_list /path/to/annotation/paths.txt \
    --labels /path/to/labels.txt \
    --output /path/to/annotations.json
```

## Training steps
 - Data preparation 
    - convert pascal voc format into coco format(use voc2coco module)
    - split annotations.json into annotations-train.json and annotations-val.json
    - put images into "data/prima/Images/" folder
    - put annotations-train.json and annotations-val.json into "data/prima/" folder
 - Make changes related to number of iteration,device and model specific parameters in config.yaml
 - run train_prima.sh for starting the training process.

## Fine tune pretrained model 
 - Data preparation 
    - convert pascal voc format into coco format(use voc2coco module)
    - split annotations.json into annotations-train.json and annotations-val.json
    - put images into "data/prima/Images/" folder
    - put annotations-train.json and annotations-val.json into "data/prima/" folder
 - Make changes related to number of iteration,device,pretrained model path and model specific parameters in config.yaml
 - Put pretrained model in "../outputs/prima/mask_rcnn_R_50_FPN_3x/" directory and create "last_checkpoint" file in same directory and write model name in this file.
 - Make RESUME True in config file.
 - run train_prima.sh(../scripts/train_prima.sh) for starting the training process.

## Reference 

- **[cocosplit](https://github.com/akarazniewicz/cocosplit)**  A script that splits the coco annotations into train and test sets.
- **[Detectron2](https://github.com/facebookresearch/detectron2)** Detectron2 is Facebook AI Research's next generation software system that implements state-of-the-art object detection algorithms. 