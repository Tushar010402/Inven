import cv2
import numpy as np
import json
from datetime import datetime, timedelta

def load_sample_data():
    with open('cans_data.json', 'r') as file:
        return json.load(file)

def create_mock_video():
    # Create a blank image
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    # Load sample data
    data = load_sample_data()
    cans = data['cans']

    # Set up font and colors
    font = cv2.FONT_HERSHEY_SIMPLEX
    white = (255, 255, 255)

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('processed_video.mp4', fourcc, 1, (640, 480))

    # Simulate video processing
    start_time = datetime.now()
    for i in range(100):  # 100 frames, each representing 1 second
        frame.fill(0)  # Clear the frame

        # Add timestamp
        current_time = start_time + timedelta(seconds=i)
        cv2.putText(frame, current_time.strftime("%Y-%m-%d %H:%M:%S"), (10, 30), font, 0.7, white, 2)

        # Display inventory counts
        y_offset = 60
        for can in cans:
            text = f"{can['product_name']}: {can['inventory_count']}"
            cv2.putText(frame, text, (10, y_offset), font, 0.7, white, 2)
            y_offset += 30

            # Simulate inventory changes
            if i % 10 == 0:  # Every 10 seconds
                can['inventory_count'] = max(0, can['inventory_count'] - np.random.randint(0, 5))

        out.write(frame)

    out.release()

def display_processed_video():
    create_mock_video()

    cap = cv2.VideoCapture('processed_video.mp4')

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Processed Video', frame)

        if cv2.waitKey(1000) & 0xFF == ord('q'):  # Wait for 1 second between frames, quit if 'q' is pressed
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_processed_video()
