# Bird tracking using ByteTrack

This repo contains tools and experiment files used for tracking birds in a cage using [ByteTrack](https://github.com/ifzhang/ByteTrack).

ByteTrack's is codebase is based on [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) object detector, and for this reason, YOLOX pretrained weights can be used for tracking with ByteTrack.

## Dataset converter

Under `tools` there's `convert_dataset.py` that can be used to convert dataset from [COCO](https://cocodataset.org/#format-data) format to ByteTrack trainable format.

Install requirements:

```
python3 -m pip install pycocotools
```

Example:

```
python3 convert_dataset.py \
         --input birds/annotations/annotations_val.json \
         --output birds/annotations/annotations_valo_preprocessed.json \
         --data-dir data \
         --ground-truth-output ByteTrack/datasets/mot/train/data/gt/gt.txt \
         --category-as-track_id \
         --coco-categories \
         --target-category 16
```

Parameters:
  * `--input`: the input COCO file
  * `--output`: the output COCO file
  * `--data-dir`: fix the image file paths in the JSON using the provided directory
  * `--ground-truth-output`: the path of ByteTrack compatible ground truth file that can be used for validation
  * `--category-as-track_id`: if set, COCO `category_id` will be used as `track_id`. It can be used when the different moving objects are categorized separately.
  * `--coco-categories`: if set, include COCO categories in the output file
  * `--target-category`: set the annotations' category to this category (`16` is the `bird`)

## Browsing the dataset

You can explore the dataset using `tools/browse_dataset.py` which uses [FiftyOne](https://voxel51.com/docs/fiftyone/).

Install requirements:

```
python3 -m pip install pandas fiftyone
```

Example:

```
python3 browse_dataset.py -i birds/annotations/annotations_valo_preprocessed.json
```


## Experiment files

The `exps` directory contains the experiment files which can be used for ByteTrack (and YOLOX) training, evaluation and tracking.

They contain model parameters and dataloading, training and evaluation configs.

  * `yolox_s_bird.py`: for training YOLOX with small network
  * `yolox_x_bird.py`: for training YOLOX with larger network
  * `bytetrack_x_bird.py`: for training ByteTrack with larger network

NOTE: if you use ByteTrack with pretrained YOLOX weight, use the weights from YOLOX `0.1.0` release (git tag), because ByteTrack is currently based on that revision.
