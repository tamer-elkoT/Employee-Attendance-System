import face_recognition 
import numpy as np
import cv2
import pickle
import os
from mtcnn import MTCNN # Import MTCNN for face detection (Multi-Task Cascaded Convolutional Neural Network)
from app.core.config import settings
import asyncio
# 1. Initialize Smart Detector (Global)
# This loads the heavy Neural Network once when the app starts.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Hide TensorFlow warnings
mtcnn_detector = MTCNN() # Initialize MTCNN face detector

# Helper : Convert Bytes to Image RGB
def load_image_from_bytes(image_bytes: bytes):
    """ Decodes raw uploaded image bytes to an RGB image array. """
    nparr = np.frombuffer(image_bytes, np.uint8) # Convert bytes to numpy array
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # Decode image from numpy array
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert BGR to RGB
    return rgb_img

# Logic : Detect Faces using MTCNN for Regesistration 
async  def detect_faces(files):
    """
    Takes a list of 5 images. Uses MTCNN to find the best face.
    Returns: Best Encoding (Bytes), Best Index (Int)
    """

    best_confidence = 0.0
    best_encoding = None
    best_index = -1

    # Iterate over the 5 photos
    for i , file in enumerate(files):
        # read image bytes
        image_bytes = await file.read()
        await file.seek(0) # Reset file pointer for future use
        # Load image from bytes to numpy RGB Array
        rgb_img = load_image_from_bytes(image_bytes)
        # Detect faces using MTCNN
        detections = mtcnn_detector.detect_faces(rgb_img) # Get list of detected faces 
        # detection is a list of dicts with 'box', 'confidence', 'keypoints'
        #         detections = [
        #     {
        #         'box': [120, 80, 160, 160],
        #         'confidence': 0.82,
        #         'keypoints': {...}
        #     },
        #     {
        #         'box': [200, 90, 150, 150],
        #         'confidence': 0.96,
        #         'keypoints': {...}
        #     }
        # ]
        if not detections:
            continue # No faces detected in this image
        # Find the detection with the highest confidence
        # max(iterable, key=function)
        if detections:
            best_detection = max(detections, key=lambda det:det["confidence"])
            confidence = best_detection["confidence"]
        else:
            best_detection = None
        
        # If confidence is higher than previous best, and above threshold, get the bounding box
        if confidence > best_confidence and confidence >= settings.CONFIDENCE_THRESHOLD:
            x, y, w, h = best_detection["box"] # Get the bounding box
            # Convert from (x, y, w, h) to (top, right, bottom, left) format 
            # Because face_recognition expects (top, right, bottom, left)
            top, right, bottom, left = max(0,y), max(0,x+w), max(0, y+h), max(0,x)
            box = [(top, right, bottom, left)] # face_recognition expects a list of boxes
            # Get the face encoding using face_recognition
            try:
                encoding = face_recognition.face_encodings(rgb_img, box) # Returns a list of encodings 
                best_confidence = confidence
                best_encoding_bytes = pickle.dumps(encoding) # Serialize encoding to bytes
                best_index = i

            except IndexError:
                continue 
    
    return best_encoding_bytes, best_index, best_confidence


def get_live_encoding(image_bytes):
    """
    Use fast HOG detector for real-time video feed.
    It takes image_bytes (raw bytes of an image captured from the camera).
    HOG (Histogram of Oriented Gradients) is a fast, CPU-friendly method to detect faces.

    """
    # Load image from bytes to numpy RGB Array
    rgb_img = load_image_from_bytes(image_bytes)
    # Detect face locations using HOG
    boxes = face_recognition.face_locations(rgb_img) # Returns list of (top, right, bottom, left) tuples
    # if no faces detected, return None
    if not boxes:
        return None
    # Get the face encodings for the detected faces
    # face_encodings generates a 128-dimensional vector that uniquely represents a face.
    # boxes tells it where the faces are.
    encoding = face_recognition.face_encodings(rgb_img, boxes)[0] # Get the first face encoding
    # Serializes the NumPy array (encoding) into bytes using pickle.
    # This allows you to store the face encoding in a database or send it over the network.
    return pickle.dumps(encoding)

def find_match(known_employees, live_encoding_bytes):
    """
    Compares the live encoding with known employee encodings to find a match.
    
    Parameters:
    - known_employees: List of Employee objects with known encodings
    - live_encoding_bytes: Serialized bytes of the live face encoding
    
    Returns:
    - matched_employee: The Employee object that matches, or None if no match found
    - match_index: Index of the matched employee in the known_employees list, or -1 if no match
    - match_distance: Distance of the best match, or None if no match
    """
    live_encoding = pickle.loads(live_encoding_bytes) # Deserialize live encoding bytes to Numpy array

    # Loop through known employees to find a match
    for emp in known_employees:
        # Convert the stored encoding for the current employee from bytes → NumPy array.
        known_encoding = pickle.loads(emp.encoding) 
        # compare the live encoding with the known encoding
        match = face_recognition.compare_faces( # compare_faces calculates the distance between the new face and known faces.
            [known_encoding], live_encoding,
            tolerance=settings.FACE_TOLRANCE # Returns True if the face matches (distance ≤ tolerance) False otherwise.
        )[0] # compare_faces returns a list of booleans indicating matches
        
        if match:
            distance = face_recognition.face_distance( # Calculate the distance between the live encoding and known encoding
                [known_encoding], live_encoding
            )[0] # face_distance returns a list of distances
        
            return emp, known_employees.index(emp), distance
    return None, -1, None # No match found
