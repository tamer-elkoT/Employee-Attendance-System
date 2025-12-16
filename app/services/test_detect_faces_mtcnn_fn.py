import asyncio
from app.services.face_logic import detect_faces_mtcnn
from io import BytesIO
import os
import pickle

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

async def test_detect_faces_mtcnn():
    best_encoding_bytes, best_index = await detect_faces_mtcnn(files)

    if best_encoding_bytes:
        print(f"Best face found in image index: {best_index}")
        encoding = pickle.loads(best_encoding_bytes)
        print(f"Encoding bytes length: {len(encoding[0])}")
    else:
        print("No faces detected in any of the images.")

asyncio.run(test_detect_faces_mtcnn())