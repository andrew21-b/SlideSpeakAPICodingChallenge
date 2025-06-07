from fastapi import FastAPI, UploadFile
from file_handling import save_img_to_temp_dir
import florence_model
import create_presentaion
import tempfile

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Welcome to SlideSpeak Xhanced"}


@app.post("/geneterate_presentation")
async def generate_presentation(image: UploadFile):
    temp_dir = tempfile.TemporaryDirectory()

    saved_img_path = await save_img_to_temp_dir(image, temp_dir.name)

    img_caption = await florence_model.get_context_caption(saved_img_path)

    temp_dir.cleanup()

    try:
        return await create_presentaion.generate_presentaion(img_caption)
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_status/{presentation_id}")
async def get_status(presentation_id: str):
    try:
        return await create_presentaion.get_status(presentation_id)
    except Exception as e:
        return {"error": str(e)}
