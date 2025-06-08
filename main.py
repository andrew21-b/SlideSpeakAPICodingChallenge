from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from file_handling import save_img_to_temp_dir
import florence_model
import create_presentaion
import tempfile

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.job_queue = []


@app.get("/")
async def read_root():
    return {"Welcome to SlideSpeak Xhanced"}


@app.post("/geneterate_presentation")
async def generate_presentation(image: UploadFile, request: Request):
    temp_dir = tempfile.TemporaryDirectory()
    saved_img_path = await save_img_to_temp_dir(image, temp_dir.name)
    img_caption = await florence_model.get_context_caption(saved_img_path)
    if (
        img_caption is None
        or img_caption == "Error generating caption from the florence model."
    ):
        temp_dir.cleanup()
        return {"error": "Failed to generate caption from the image."}

    temp_dir.cleanup()

    job_id = await create_presentaion.generate_presentaion(img_caption)

    job = await create_presentaion.get_status(job_id)

    manage_job_queue(request, job)

    return {"job_id": job_id}


@app.get("/get_status/{presentation_id}")
async def get_status(presentation_id: str):
    try:
        return await create_presentaion.get_status(presentation_id)
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_queue")
async def get_queue(request: Request):
    job_queue = request.app.state.job_queue
    new_job_queue = []
    for job in job_queue:
        job_id = job.get("task_id")
        updated_job = await create_presentaion.get_status(job_id)
        new_job_queue.append(updated_job)
    job_queue = new_job_queue

    return {"jobs": job_queue}


def manage_job_queue(request, job):
    if len(request.app.state.job_queue) < 5:
        request.app.state.job_queue.append(job)
    else:
        request.app.state.job_queue.pop(0)
        request.app.state.job_queue.append(job)
