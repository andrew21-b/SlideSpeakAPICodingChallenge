import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import asyncio
import tempfile
from fastapi import UploadFile
from file_handling import save_img_to_temp_dir
from florence_model import get_context_caption

@pytest.mark.skipif(os.getenv("LOCAL_MACHINE") == None, reason="can only bne run on a local machine")
def test_evnvironemt_variable_returns_api_key():
    env_variable = os.getenv("SLIDESPEAK_API_KEY")

    assert env_variable is not None
    assert isinstance(env_variable, str)
    assert len(env_variable) > 4


def test_florence_model_returns_caption():

    sample_image_path = "images/bottle.jpg"
    caption = asyncio.run(get_context_caption(sample_image_path))

    assert isinstance(caption, str)
    assert len(caption) > 0


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
