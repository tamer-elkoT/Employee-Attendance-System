import asyncio
from app.services.face_logic import detect_faces
from io import BytesIO
import os
import pickle
import cv2
import matplotlib.pyplot as plt

class FakeUploadFile:
    def __init__(self,path):
        self.path = path
        self.file =open(path,"rb")

    async def read(self):
        self.file.seek(0)
        return self.file.read()
    
    async def seek(self,pos):
        self.file.seek(pos)

images_paths = [
    "app/test images/1751386829283.jpg",
    "app/test images/IMG-20250308-WA0002 (1).png",
    "app/test images/Me.png",
    "app/test images/WhatsApp Image 2025-07-15 at 03.41.31_c171f600.jpg",
    "app/test images/WhatsApp Image 2025-10-30 at 00.35.45_3a1f571c.jpg"

]

files = [FakeUploadFile(path) for path in images_paths]

async def show_best_face():
    # Get the best face info
    best_encoding_bytes, best_index, best_confidence = await detect_faces(files)

    if best_index != -1:
        best_image_path = images_paths[best_index]
        print(f"Best face found in image index: {best_index}")
        print(f"Confidence", best_confidence)
        encoding = pickle.loads(best_encoding_bytes)
        print(f"Encoding bytes length: {len(encoding[0])}")
        print(f"Best image path", best_image_path)

        # load and show the image
        img = cv2.imread(best_image_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
        plt.axis("off")
        plt.show(block=True)
    else:
        print("No faces detected in any of the images.")
# Run the async function
asyncio.run(show_best_face())

