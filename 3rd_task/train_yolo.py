from datasets import load_dataset, DatasetDict
from ultralytics import YOLO
import os
import pandas as pd

# 1. CPPE-5 데이터셋 로드 및 train → train/val 분할
ds = load_dataset("rishitdagli/cppe-5")
split_ds = ds["train"].train_test_split(test_size=0.2, seed=42)
ds = DatasetDict({
    "train": split_ds["train"],
    "val": split_ds["test"],
    "test": ds["test"]
})

# 2. YOLO 학습을 위한 디렉토리 생성
base_dir = "3rd_task/datasets"
for split in ["train", "val", "test"]:
    os.makedirs(f"{base_dir}/images/{split}", exist_ok=True)
    os.makedirs(f"{base_dir}/labels/{split}", exist_ok=True)

# 3. YOLO 포맷 저장 함수
def save_yolo_format(example, split):
    image = example["image"]
    id = example["image_id"]
    file_name = f"{id}.jpg"
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(f"{base_dir}/images/{split}/{file_name}")
    h, w = example["height"], example["width"]
    label_path = f"{base_dir}/labels/{split}/{id}.txt"
    with open(label_path, "w") as f:
        for bbox, class_id in zip(example["objects"]["bbox"], example["objects"]["category"]):
            x_center = (bbox[0] + bbox[2] / 2) / w
            y_center = (bbox[1] + bbox[3] / 2) / h
            bw = bbox[2] / w
            bh = bbox[3] / h
            f.write(f"{class_id} {x_center} {y_center} {bw} {bh}\n")

# 4. 전체 split에 대해 YOLO 포맷 저장
for split in ["train", "val", "test"]:
    for example in ds[split]:
        save_yolo_format(example, split)

# 5. YOLO 학습
model = YOLO("/Users/sonjiyeon/Desktop/CV_project/3rd_task/yolov8n.pt")
model.train(data="/Users/sonjiyeon/Desktop/CV_project/3rd_task/data.yaml", epochs=30, imgsz=640,name="yolo_train",save=True)
