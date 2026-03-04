import os
import shutil
from typing import List
from app.api.services.blob_service import upload_file_path
from ultralytics import YOLO

model = YOLO(os.path.join("app/yolo_models/v11n.pt"))


class DetectImagesResponse:
    image_url: str
    image_url_result: str
    result: dict


def detect_images(images: List[str]) -> List[DetectImagesResponse]:

    results = model.predict(images, save=True)

    images_results = []

    for index, result in enumerate(results):
        detections = []
        image_path_result = os.path.join(result.save_dir, os.path.basename(result.path))

        new_image = upload_file_path(image_path_result)

        for box in result.boxes:
            x, y, w, h = box.xywh[0].tolist()

            detections.append(
                {
                    "class": result.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": {"x": x, "y": y, "w": w, "h": h},
                }
            )

        if os.path.exists(image_path_result):
            os.remove(image_path_result)

        if os.path.isdir(result.save_dir):
            if not os.listdir(result.save_dir):
                shutil.rmtree(result.save_dir)

        images_results.append(
            {
                "image_url": images[index],
                "image_url_result": new_image,
                "result": detections,
            }
        )

    return images_results
