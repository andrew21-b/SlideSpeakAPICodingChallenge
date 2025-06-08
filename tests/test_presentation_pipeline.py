import io
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
import asyncio
import tempfile
from fastapi import UploadFile
from fastapi.testclient import TestClient
from file_handling import save_img_to_temp_dir
from florence_model import get_context_caption
from create_presentaion import generate_presentaion, get_status
from main import app, manage_job_queue


client = TestClient(app)


@pytest.mark.skipif(
    os.getenv("LOCAL_MACHINE") == None, reason="can only run on a local machine"
)
def test_evnvironemt_variable_returns_api_key():
    env_variable = os.getenv("SLIDESPEAK_API_KEY")

    assert env_variable is not None
    assert isinstance(env_variable, str)
    assert len(env_variable) > 4


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("SLIDESPEAK_API_KEY", raising=False)
    assert os.getenv("SLIDESPEAK_API_KEY") is None


def test_florence_model_returns_caption():

    sample_image_path = "images/bottle.jpg"
    caption = get_context_caption(sample_image_path)

    assert isinstance(caption, str)
    assert len(caption) > 0


def test_florence_model_with_invalid_image_path():

    sample_image_path = "images/bottle_invalid.jpg"
    caption = get_context_caption(sample_image_path)

    assert isinstance(caption, str)
    assert (
        caption == "Error: Image path does not exist."
        or caption == "Error generating caption from the florence model."
    )


def test_save_img_to_temp_dir_creates_file():

    sample_image_path = "images/bottle.jpg"
    with open(sample_image_path, "rb") as f:
        upload_file = UploadFile(filename=os.path.basename(sample_image_path), file=f)
        with tempfile.TemporaryDirectory() as temp_dir:
            saved_img_path = asyncio.run(save_img_to_temp_dir(upload_file, temp_dir))

            assert saved_img_path is not None
            assert os.path.exists(saved_img_path)
            assert os.path.isfile(saved_img_path)
            assert saved_img_path.endswith(".jpg") or saved_img_path.endswith(".png")


def test_save_img_to_temp_dir_with_non_image():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(__file__, "rb") as f:
            upload_file = UploadFile(filename="not_an_image.txt", file=f)
            saved_img_path = asyncio.run(save_img_to_temp_dir(upload_file, temp_dir))
            assert (
                saved_img_path is None
                or saved_img_path
                == "Unsupported image format. Only JPEG and PNG are allowed."
            )


@pytest.mark.skipif(os.getenv("SLIDESPEAK_API_KEY") is None, reason="API key required")
def test_generate_presentation_returns_job_id():
    prompt = "Test prompt"
    job_id = generate_presentaion(prompt)
    assert isinstance(job_id, str)
    assert len(job_id) > 0


def test_get_status_with_invalid_job_id():
    invalid_job_id = "nonexistent"
    result = get_status(invalid_job_id)
    assert isinstance(result, tuple) or isinstance(result, dict)


def test_generate_presentation_handles_rate_limit(monkeypatch):
    class MockResponse:
        def __init__(self, status_code=429, json_data=None):
            self.status_code = status_code
            self._json_data = json_data or {"error": "Rate limit exceeded"}

        def json(self):
            return self._json_data

    def mock_post(*args, **kwargs):
        return MockResponse(429, {"error": "Rate limit exceeded"})

    monkeypatch.setattr(requests, "post", mock_post)

    prompt = "Test prompt"
    result = generate_presentaion(prompt)
    print(result)
    assert result == None


def test_generate_presentation_success(monkeypatch):
    import florence_model
    import create_presentaion

    monkeypatch.setattr(
        florence_model, "get_context_caption", lambda path: "A test caption"
    )

    monkeypatch.setattr(
        create_presentaion, "generate_presentaion", lambda caption: "fake_job_id"
    )

    monkeypatch.setattr(
        create_presentaion,
        "get_status",
        lambda job_id: {"task_id": job_id, "task_status": "PENDING"},
    )

    file_content = io.BytesIO(b"fake image data")
    response = client.post(
        "/geneterate_presentation",
        files={"image": ("test.jpg", file_content, "image/jpeg")},
    )

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["job_id"] == "fake_job_id"


def test_manage_job_queue_adds_and_limits(monkeypatch):
    class DummyState:
        def __init__(self):
            self.job_queue = []

    class DummyApp:
        def __init__(self):
            self.state = DummyState()

    class DummyRequest:
        app = DummyApp()

    for i in range(5):
        job = {"task_id": f"id_{i}", "task_status": "PENDING"}
        manage_job_queue(DummyRequest, job)
    assert len(DummyRequest.app.state.job_queue) == 5

    new_job = {"task_id": "id_5", "task_status": "PENDING"}
    manage_job_queue(DummyRequest, new_job)

    assert len(DummyRequest.app.state.job_queue) == 5
    assert (
        DummyRequest.app.state.job_queue[0]["task_id"] == "id_1"
    ) 


def test_get_queue_returns_updated_jobs(monkeypatch):
    app.state.job_queue = [
        {"task_id": "id_1", "task_status": "PENDING"},
        {"task_id": "id_2", "task_status": "PENDING"},
    ]

    
    import create_presentaion

    def mock_get_status(job_id):
        return {"task_id": job_id, "task_status": "SUCCESS"}

    monkeypatch.setattr(create_presentaion, "get_status", mock_get_status)

    response = client.get("/get_queue")
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert all(job["task_status"] == "SUCCESS" for job in data["jobs"])
    assert len(data["jobs"]) == 2
