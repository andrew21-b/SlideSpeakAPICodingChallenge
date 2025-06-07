from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForCausalLM


async def get_context_caption(image_path: str) -> str:
    model_id = "microsoft/Florence-2-large"
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, torch_dtype="auto"
        )
        .eval()
        .cuda()
    )
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    prompt = "<CAPTION>"

    image = Image.open(image_path)

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(
        "cuda", torch.float16
    )

    generated_ids = model.generate(
        input_ids=inputs["input_ids"].cuda(),
        pixel_values=inputs["pixel_values"].cuda(),
        max_new_tokens=1024,
        early_stopping=True,
        do_sample=False,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(
        generated_text, task=prompt, image_size=(image.width, image.height)
    )

    return parsed_answer[prompt]
