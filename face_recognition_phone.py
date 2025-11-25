import face_recognition
import cv2
import numpy as np
import time
import pickle


# ===========================
# ?? CONFIGURATION
# ===========================
# Replace this with your phone's IP Webcam stream URL
PHONE_CAM_URL = "http://172.16.12.115:8080/video"  # <- Change this IP!
cv_scaler = 4  # Scale factor for performance (lower = more accurate but slower)

# ===========================
# ?? LOAD ENCODINGS
# ===========================
print("[INFO] Loading face encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# ===========================
# ?? INITIALIZE PHONE CAMERA
# ===========================
print("[INFO] Connecting to phone camera stream...")
cap = cv2.VideoCapture(PHONE_CAM_URL)
if not cap.isOpened():
    raise Exception("? Could not connect to the phone camera stream. Check IP and network connection!")

# Optional: force resolution (depends on IP Webcam settings)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ===========================
# ?? FACE RECOGNITION LOOP
# ===========================
face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0

def process_frame(frame):
    global face_locations, face_encodings, face_names

    # Resize the frame for faster processing
    resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))
    
    # Convert BGR (OpenCV) ? RGB (face_recognition)
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces and get encodings
    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')
    
    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        # Pick the best match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        face_names.append(name)
    
    return frame

def draw_results(frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face coordinates
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler
        
        # Draw bounding box
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        cv2.rectangle(frame, (left - 3, top - 35), (right + 3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
    
    return frame

def calculate_fps():
    global frame_count, start_time, fps
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return fps

# ===========================
# ??? MAIN LOOP
# ===========================
print("[INFO] Starting face recognition... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("?? Failed to grab frame. Check phone connection.")
        break

    processed_frame = process_frame(frame)
    display_frame = draw_results(processed_frame)

    # Show FPS
    current_fps = calculate_fps()
    cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Display
    cv2.imshow('Face Recognition', display_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ===========================
# ?? CLEANUP
# ===========================
cap.release()
cv2.destroyAllWindows()
print("[INFO] Face recognition stopped.")
