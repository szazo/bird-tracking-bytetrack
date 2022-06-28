import argparse
from os import path

import fiftyone as fo

parser = argparse.ArgumentParser('COCO dataset browser using FiftyOne')
parser.add_argument('-i', '--input', required=True, default=None, type=str,
                    help='Input JSON file')

args = parser.parse_args()

input_filepath = args.input
input_dir = path.split(input_filepath)[0]

dataset = fo.Dataset.from_dir(
    data_path=input_dir,
    labels_path=input_filepath,
    dataset_type=fo.types.COCODetectionDataset,
    label_field='detections',
)

session = fo.launch_app(dataset)
session.wait()
