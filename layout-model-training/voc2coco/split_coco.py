import json
import argparse
import funcy
from sklearn.model_selection import train_test_split


def save_coco(file,  images, annotations, categories):
    with open(file, 'wt', encoding='UTF-8') as coco:
        json.dump({ 'images': images, 
            'annotations': annotations, 'categories': categories}, coco, indent=2, sort_keys=True)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: str(i['id']), images)
    return funcy.lfilter(lambda a: str(a['image_id']) in image_ids, annotations)

def main(annotation_path,
         split_ratio,
         having_annotations,
         train_save_path,
         test_save_path,
         random_state=None):

    with open(annotation_path, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)
        #info = coco['info']
        #licenses = coco['licenses']
        images = coco['images']
        annotations = coco['annotations']
        categories = coco['categories']

        number_of_images = len(images)

        images_with_annotations = funcy.lmap(lambda a: str(a['image_id']), annotations)

        if having_annotations:
            images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

        x, y = train_test_split(images, train_size=split_ratio, random_state=random_state)

        save_coco(train_save_path, x, filter_annotations(annotations, x), categories)
        save_coco(test_save_path,  y, filter_annotations(annotations, y), categories)

        print("Saved {} entries in {} and {} in {}".format(len(x), train_save_path, len(y), test_save_path))
parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
parser.add_argument('annotations', metavar='coco_annotations', type=str,
                    help='Path to COCO annotations file.')
parser.add_argument('train', type=str, help='Where to store COCO training annotations')
parser.add_argument('test', type=str, help='Where to store COCO test annotations')
parser.add_argument('-s', dest='split_ratio', type=float, required=True,
                    help="A percentage of a split; a number in (0, 1)")
parser.add_argument('--having-annotations', dest='having_annotations', action='store_true',
                    help='Ignore all images without annotations. Keep only these with at least one annotation')

    
#parser.add_argument('--annotation_path',  type=str, metavar='/home/naresh/Tarento/voc2coco/sample/output.json', help='the path of annotations')
annotation_path= '/home/naresh/Tarento/primalaynet/layout-model-training/tools/prima_line_training_data_v1/annotations.json'
if __name__ == "__main__":
    

    parser.split_ratio =0.95
    parser.having_annotations=True
    main(annotation_path,
         parser.split_ratio,
         parser.having_annotations, 
         train_save_path=annotation_path.replace('.json', '-train.json'),
         test_save_path=annotation_path.replace('.json', '-val.json'),
         random_state=24)
