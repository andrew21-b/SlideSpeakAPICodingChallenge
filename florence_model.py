import os
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForCausalLM


def get_context_caption(image_path: str) -> str:

    if os.path.exists(image_path) is False:
        print(f"Image path {image_path} does not exist.")
        return "Error: Image path does not exist."

    try:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "microsoft/Florence-2-large"
        model = AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, torch_dtype=torch_dtype
        ).to(device=device)

        processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

        prompt = "<CAPTION>"

        image = Image.open(image_path)

        inputs = processor(text=prompt, images=image, return_tensors="pt").to(
            device, torch_dtype
        )

        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            early_stopping=True,
            do_sample=False,
            num_beams=3,
        )

        generated_text = processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]

        parsed_answer = processor.post_process_generation(
            generated_text, task=prompt, image_size=(image.width, image.height)
        )

        return parsed_answer[prompt]
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "Error generating caption from the florence model."
