from sqlalchemy.orm import Session
from app.api.models.detection import Detection


def create_detections(db: Session, detections: list) -> list:
    db.add_all(detections)
    db.commit()
    for d in detections:
        db.refresh(d)
    return detections


def get_all_by_user(db: Session, user_id) -> list:
    return db.query(Detection).filter(Detection.user_id == user_id).all()


def get_by_id(db: Session, detection_id: str, user_id) -> Detection | None:
    return (
        db.query(Detection)
        .filter(Detection.id == detection_id, Detection.user_id == user_id)
        .first()
    )


def delete_by_id(db: Session, detection: Detection) -> None:
    db.delete(detection)
    db.commit()


def delete_all_by_user(db: Session, user_id) -> None:
    db.query(Detection).filter(Detection.user_id == user_id).delete()
    db.commit()
