from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.api.services import blob_service
from app.api.deps import get_current_user, get_db
from app.api.models.detection import Detection
from app.api.services.detector_service import detect_images
from app.api.repositories import detection_repository

router = APIRouter(tags=["detection"])


@router.post("/detect")
def detect(
    files: List[UploadFile] = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    imgs = []
    for img in files:
        if not img.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")
        imgs.append(blob_service.upload_image(img))

    results = detect_images(imgs)

    models = [
        Detection(
            image_url=result["image_url"],
            result=result["result"],
            image_url_result=result["image_url_result"],
            user_id=current_user.id,
        )
        for result in results
    ]

    saved = detection_repository.create_detections(db, models)

    return [
        {
            "id": str(d.id),
            "image_url": d.image_url,
            "result": d.result,
            "image_url_result": d.image_url_result,
            "user_id": str(d.user_id),
        }
        for d in saved
    ]


@router.get("/detections")
def get_detections(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return detection_repository.get_all_by_user(db, current_user.id)


@router.get("/detections/{detection_id}")
def get_detection(
    detection_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detection = detection_repository.get_by_id(db, detection_id, current_user.id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection não encontrada")
    return detection


@router.delete("/detections/{detection_id}")
def delete_detection(
    detection_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    detection = detection_repository.get_by_id(db, detection_id, current_user.id)
    if not detection:
        raise HTTPException(status_code=404, detail="Detection não encontrada")
    detection_repository.delete_by_id(db, detection)
    return {"message": "Detection apagada com sucesso"}


@router.delete("/detections")
def delete_all_detections(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    detection_repository.delete_all_by_user(db, current_user.id)
    return {"message": "Todas as detections apagadas com sucesso"}
