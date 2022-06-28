# Bird tracking using ByteTrack

This repo contains tools and experiment files used for tracking birds in a cage using [ByteTrack](https://github.com/ifzhang/ByteTrack).

ByteTrack's is codebase is based on [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX) object detector, and for this reason, YOLOX pretrained weights can be used for tracking with ByteTrack.

## Dataset converter

Under `tools` there's `convert_dataset.py` that can be used to convert dataset from [COCO](https://cocodataset.org/#format-data) format to ByteTrack trainable format.

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
