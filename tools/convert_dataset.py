import argparse
from pycocotools.coco import COCO
from coco_categories import coco_categories
from os import path
import json

def make_parser():
    parser = argparse.ArgumentParser('Birds COCO to YOLOX converter')
    parser.add_argument('-i', '--input', required=True, default=None, type=str, help='input file')
    parser.add_argument('-o', '--output', required=True, default=None, type=str, help='output file')
    parser.add_argument('-d', '--data-dir', default='data', type=str, help='The data directory of the images')
    parser.add_argument('--coco-categories', action='store_true', help='Use COCO categories in output')
    parser.add_argument('-t', '--target-category', default=None, type=int, help='Replace category of the boxes')
    parser.add_argument('--category-as-track_id', action='store_true', help='Use category_id as track_id that can be used for MOT evaluation')

    return parser

args = make_parser().parse_args()

print('args', args)

input_filepath = args.input
out_filepath = args.output
data_dir = args.data_dir

coco = COCO(annotation_file=input_filepath)
ds = coco.dataset

categories = ds['categories']
if args.coco_categories:
    categories = coco_categories

use_category_as_track_id = args.category_as_track_id
#counts = dataset.count_values("ground_truth.detections.label")

# https://stackoverflow.com/questions/60227833/how-to-filter-coco-dataset-classes-annotations-for-custom-dataset

annotations = []
image_ids = []
for annotation in ds['annotations']:
    current_category_id = annotation['category_id']
    if args.target_category is not None:
        annotation['category_id'] = args.target_category

    track_id = current_category_id if use_category_as_track_id else -1
    annotation['track_id'] = track_id
    annotations.append(annotation)

    image_id = annotation['image_id']
    if image_id not in image_ids:
        image_ids.append(image_id)
    #break


input_images = coco.loadImgs(image_ids)
images = []
image_index = 0
for image in input_images:
    file_name = image['file_name']
    tail = path.split(file_name)[1]
    file_name = path.join(data_dir, tail)
    image['file_name'] = file_name
    image['video_id'] = 1 # we have only one video
    image['frame_id'] = image_index + 1 # image number in the video sequence, starting from 1
    images.append(image)
    image_index += 1
    #break

out = {
    'info': ds['info'],
    'licenses': ds['licenses'],
    'images': images,
    'annotations': annotations,
    'categories': categories
}

#print(out)

with open(out_filepath, 'w') as f:
    json.dump(out, f, indent=4)

#anns = ds['annotations']
#print(len(anns))
#print(anns)

#for ann in anns:
#    print(ann)
#print(counts)

#session = fo.launch_app(dataset)
print(len(coco_categories))
