import argparse
from pycocotools.coco import COCO
from coco_categories import coco_categories
from os import path
import json

def make_parser():
    parser = argparse.ArgumentParser('Birds COCO to YOLOX converter')
    parser.add_argument('-i', '--input', required=True, default=None, type=str, help='Input file')
    parser.add_argument('-o', '--output', required=True, default=None, type=str, help='Output file')
    parser.add_argument('-d', '--data-dir', default='data', type=str, help='The data directory of the images')
    parser.add_argument('--coco-categories', action='store_true', help='Use COCO categories in output')
    parser.add_argument('-t', '--target-category', default=None, type=int, help='Replace category of the boxes')
    parser.add_argument('--category-as-track_id', action='store_true', help='Use category_id as track_id that can be used for MOT evaluation')
    parser.add_argument('-gt', '--ground-truth-output', default=None, type=str, help='Ground truth (gt.txt) output file')

    return parser

args = make_parser().parse_args()

print('args', args)

input_filepath = args.input
out_filepath = args.output
gt_out_filepath = args.ground_truth_output
data_dir = args.data_dir

coco = COCO(annotation_file=input_filepath)
ds = coco.dataset

categories = ds['categories']
if args.coco_categories:
    categories = coco_categories

use_category_as_track_id = args.category_as_track_id
#counts = dataset.count_values("ground_truth.detections.label")

# https://stackoverflow.com/questions/60227833/how-to-filter-coco-dataset-classes-annotations-for-custom-dataset

ground_truth = []

annotations = []
image_ids = []
for annotation in ds['annotations']:
    current_category_id = annotation['category_id']
    if args.target_category is not None:
        annotation['category_id'] = args.target_category

    track_id = current_category_id if use_category_as_track_id else -1
    annotation['track_id'] = track_id

    image_id = annotation['image_id']
    if image_id not in image_ids:
        image_ids.append(image_id)
    #break

    bbox = annotation['bbox']
    ground_truth.append({
        'image_id': image_id,  # for determining frame id later
        'id': track_id,
        'box': {
            'left': bbox[0],
            'top': bbox[1],
            'width': bbox[2],
            'height': bbox[3]
        },
        'conf': 1,
        'x': -1,  # only required for 3D
        'y': -1,
        'z': -1
    })

    # store the annotation
    annotations.append(annotation)

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

# determine frame ids for ground truth items
for gt in ground_truth:
    image_id = gt['image_id']
    image = next(image for image in images if image['id'] == image_id)
    print('frame', image['frame_id'])
    gt['frame'] = image['frame_id']

print('ground', ground_truth)

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
# write ground truth
if gt_out_filepath is not None:

    lines = map(lambda x: '{},{},{},{},{},{},{},{},{},{}\n'.format(
        x['frame'],
        x['id'],
        x['box']['left'],
        x['box']['top'],
        x['box']['width'],
        x['box']['height'],
        x['conf'],
        x['x'],
        x['y'],
        x['z']), ground_truth)

    with open(gt_out_filepath, 'w') as f:
        f.writelines(lines)
