import base64
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from celery import shared_task
from .models import ImageResult

@shared_task
def texttoimage(prompt):
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = settings.STABILITY_API_KEY

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    if not data.get("artifacts"):
        raise Exception("No image artifacts found in the response.")
    image = data["artifacts"][0]

    image_data = base64.b64decode(image["base64"])
    result_filename = f"{prompt[:5]}_image.png"
    result_filepath = os.path.join(settings.MEDIA_ROOT, result_filename)

    with open(result_filepath, 'wb') as f:
        f.write(image_data)

    with open(result_filepath, 'rb') as f:
        image_file = ContentFile(f.read(), result_filename)
        ImageResult.objects.create(prompt=prompt, image=image_file)
    os.remove(result_filepath)

    return prompt
