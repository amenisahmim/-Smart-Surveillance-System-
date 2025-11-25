
import cv2
import os
from datetime import datetime
import time

# Change this to your phone IP and port from the IP Webcam app
PHONE_CAM_URL = "http://172.16.12.115:8080/video"  # <- replace with your actual phone IP
PERSON_NAME = "jaryd"

def create_folder(name):
    dataset_folder = "dataset"
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    
    person_folder = os.path.join(dataset_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    return person_folder

def capture_photos(name):
    folder = create_folder(name)
    
    # Use the phone camera stream instead of Picamera2
    cap = cv2.VideoCapture(PHONE_CAM_URL)

    if not cap.isOpened():
        print("? Error: Could not connect to the phone camera stream.")
        return
    
    # Set desired frame size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    # Allow stream to stabilize
    time.sleep(2)
    photo_count = 0
    
    print(f"Taking photos for {name}. Press SPACE to capture, 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("?? Failed to grab frame. Check connection.")
            break

        cv2.imshow('Capture', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord(' '):  # Space key
            photo_count += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(folder, filename)
            cv2.imwrite(filepath, frame)
            print(f"?? Photo {photo_count} saved: {filepath}")
        
        elif key == ord('q'):  # Q key
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"? Photo capture completed. {photo_count} photos saved for {name}.")

if __name__ == "__main__":
    capture_photos(PERSON_NAME)
