import cv2
import numpy as np
from ultralytics import YOLO
import requests
import json
from datetime import datetime

# Initialize YOLOv8 model
model = YOLO('yolov8n.pt')  # Use the appropriate model for your use case

# Define classes for detection
classes = ['beer_can', 'whiskey_bottle', 'wine_bottle', 'person']

# Initialize counters for stock tracking
stock_count = {cls: 0 for cls in classes[:3]}  # Only count products, not people

# Cloud server API endpoint
API_ENDPOINT = "http://localhost:5000/api/data"

def detect_objects(frame):
    results = model(frame)
    detections = []

    # Define class mappings (adjust these based on the most suitable COCO classes)
    class_mappings = {
        0: 'person',
        39: 'bottle',  # Map bottle to represent beer, whiskey, and wine
    }

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            cls = int(box.cls[0])
            print(f"Detected class index: {cls}")  # Log the detected class index
            if conf > 0.5 and cls in class_mappings:  # Confidence threshold and class filter
                mapped_class = class_mappings[cls]
                detections.append((mapped_class, (x1, y1, x2, y2)))
            else:
                print(f"Ignored detection: class {cls}, confidence {conf}")

    return detections

def track_stock(detections):
    for cls, _ in detections:
        if cls in stock_count:
            stock_count[cls] += 1

def detect_unauthorized_activity(detections):
    person_count = sum(1 for cls, _ in detections if cls == 'person')
    if person_count > 1:
        return "Potential unauthorized activity detected"
    return None

def send_data_to_server(stock_data, event_data):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "stock_count": stock_data,
        "event": event_data
    }
    try:
        response = requests.post(API_ENDPOINT, json=payload)
        response.raise_for_status()
        print("Data sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

def main():
    global stock_count
    stock_count = {cls: 0 for cls in classes[:3]}  # Initialize stock_count inside main
    cap = cv2.VideoCapture('/home/ubuntu/SampleVideo_1280x720_1mb.mp4')  # Use a video file for testing

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_objects(frame)
        track_stock(detections)
        event = detect_unauthorized_activity(detections)

        # Visualize detections (optional)
        for cls, (x1, y1, x2, y2) in detections:
            print(f"Detected: {cls} at ({x1}, {y1}, {x2}, {y2})")

        # Send data to server every 5 minutes (adjust as needed)
        if datetime.now().minute % 5 == 0:
            send_data_to_server(stock_count, event)
            stock_count = {cls: 0 for cls in classes[:3]}  # Reset counters

    cap.release()

if __name__ == "__main__":
    main()
