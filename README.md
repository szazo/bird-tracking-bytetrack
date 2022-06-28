# Bird tracking using ByteTrack

This repo contains tools and experiments files used for tracking birds in a cage using ByteTrack.

ByteTrack's is codebase is based on YOLOX, and for this reason, YOLOX pretrained weights can be used for tracking with ByteTrack.

## Dataset converter

Under `tools` there's `convert_dataset.py` that can be used to convert dataset from COCO format to ByteTrack trainable format.

Example:

```
!python3 bird-tracking-bytetrack/tools/convert_dataset.py --category-as-track_id --coco-categories --target-category 16 \
         --input birds/annotations/annotations_val.json --output birds/annotations/annotations_valo_preprocessed.json --ground-truth-output ByteTrack/datasets/mot/train/data/gt/gt.txt
```