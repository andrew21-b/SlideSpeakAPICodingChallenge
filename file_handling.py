from fastapi import UploadFile


async def save_img_to_temp_dir(image: UploadFile, temp_dir) -> str:
    image_path = f"{temp_dir}/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    f.close()
    return image_path
