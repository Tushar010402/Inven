import cv2
import numpy as np
from ultralytics import YOLO
from collections import Counter

class YOLOIntegration:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.product_classes = {
            0: "Kingfisher",
            1: "Elephant",
            2: "Tubourg",
            3: "Budweiser"
        }

    def process_video(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        inventory_changes = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            results = self.model(frame)

            detections = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    class_id = int(box.cls[0])
                    conf = box.conf[0]
                    detections.append((self.product_classes[class_id], conf))
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f"{self.product_classes[class_id]} {conf:.2f}", (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            inventory_changes.append(Counter(d[0] for d in detections))
            out.write(frame)

            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames")

        cap.release()
        out.release()

        return inventory_changes

    def update_inventory(self, inventory_changes):
        total_changes = Counter()
        for change in inventory_changes:
            total_changes += change

        return dict(total_changes)

def main():
    yolo = YOLOIntegration("yolov8n.pt")  # Use a pre-trained model or your custom trained model
    video_path = "sample_store_video.mp4"
    output_path = "processed_video.mp4"

    inventory_changes = yolo.process_video(video_path, output_path)
    updated_inventory = yolo.update_inventory(inventory_changes)

    print("Inventory Update:")
    for product, count in updated_inventory.items():
        print(f"{product}: {count}")

if __name__ == "__main__":
    main()
