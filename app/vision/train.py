from ultralytics import YOLO
from pathlib import Path
import yaml

dataset_dir = Path(__file__).parent / "dataset"

config = {
    "path": str(dataset_dir),
    "train": "train/images",
    "val": "valid/images",
    "nc": 2,
    "names": ["not_safety_shoe", "safety_shoe"],
}

yaml_path = Path(__file__).parent / "dataset.yaml"
with open(yaml_path, "w") as f:
    yaml.dump(config, f)

model = YOLO("yolo11n.pt")
model.train(
    data=str(yaml_path),
    epochs=500,
    imgsz=640,
    batch=16,
    augment=True,
    degrees=10,
    fliplr=0.5,
    mosaic=1.0,
)
