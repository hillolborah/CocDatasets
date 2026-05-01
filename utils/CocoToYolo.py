import os
from pycocotools.coco import COCO

# ---------------- CONFIG ----------------

# COCO annotation file (CVAT export)
COCO_JSON = r"CvatExport\val_coco_annotations\annotations\instances_Validation.json"

# Dataset root
DATASET_ROOT = r"RawResized"

IMAGES_TRAIN = os.path.join(DATASET_ROOT, "images", "val")
LABELS_TRAIN = os.path.join(DATASET_ROOT, "labels", "val")

os.makedirs(LABELS_TRAIN, exist_ok=True)

# ----------------------------------------

coco = COCO(COCO_JSON)

# Build a fast lookup of available train images
train_images = set(os.listdir(IMAGES_TRAIN))


def convert_bbox(img_w, img_h, bbox):
    """COCO bbox → YOLO normalized bbox"""
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_w
    y_center = (y + h / 2) / img_h
    w /= img_w
    h /= img_h
    return x_center, y_center, w, h


for img_id, img in coco.imgs.items():
    file_name = img["file_name"]

    # Skip images not present in train/
    if file_name not in train_images:
        continue

    img_w = img["width"]
    img_h = img["height"]

    ann_ids = coco.getAnnIds(imgIds=img_id)
    anns = coco.loadAnns(ann_ids)

    label_path = os.path.join(
        LABELS_TRAIN,
        os.path.splitext(file_name)[0] + ".txt"
    )

    with open(label_path, "w") as f:
        for ann in anns:
            # YOLO uses 0-based class indices
            class_id = ann["category_id"] - 1

            x_c, y_c, w, h = convert_bbox(img_w, img_h, ann["bbox"])
            f.write(f"{class_id} {x_c} {y_c} {w} {h}\n")

print("✅ COCO → YOLO conversion completed (train-only).")
