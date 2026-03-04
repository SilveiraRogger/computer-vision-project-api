from ultralytics import YOLO

model = YOLO("vision/best.pt")

results = model.predict("vision/test.jpeg", save=True)
