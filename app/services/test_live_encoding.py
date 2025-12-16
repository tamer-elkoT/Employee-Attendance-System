import pickle
from app.services.face_logic import get_live_encoding, find_match
from app.models.employee import Employee
import cv2

# Create some fake employees 
images_paths = [
    "app/test images/1751386829283.jpg",
    "app/test images/IMG-20250308-WA0002 (1).png",
    "app/test images/Me.png"
]

class FakeEmployee:
    def __init__(self, name, department, image_path):
        self.name = name
        self.department = department
        
        img = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_bytes = cv2.imencode(".jpg",img_rgb)[1].tobytes()
        encoding = get_live_encoding(img_bytes)
        self.encoding = encoding


know_employees = [FakeEmployee(f"Employee{i+1}", "AI", path) for i, path in enumerate(images_paths)]

live_img_path = "app/test images/WhatsApp Image 2025-10-30 at 00.35.45_3a1f571c.jpg"
img = cv2.imread(live_img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_bytes = cv2.imencode(".jpg",img_rgb)[1].tobytes()
live_encoding_bytes= get_live_encoding(img_bytes)


# Test finding a match
match_employee, match_index, match_distance = find_match(know_employees, live_encoding_bytes)

if match_employee:
    print(f"Matched employee: {match_employee.name}")
    print(f"Index in known_employees: {match_index}")
    print(f"Face distance: {match_distance}")
else:
    print("No match found")