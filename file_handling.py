import os
from fastapi import UploadFile


async def save_img_to_temp_dir(image: UploadFile, temp_dir) -> str:
    filename = image.filename
    if not filename:
        return "Error: No filename provided."
    file_ext = ""
    if "." in filename:
        file_ext = "." + filename.split(".")[-1]
        if file_ext not in [".jpg", ".jpeg" ".png"]:
            return "Unsupported image format. Only JPEG and PNG are allowed."
    image_path = f"{temp_dir}/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    f.close()
    return image_path
