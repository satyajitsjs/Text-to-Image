from django.conf import settings
from celery import shared_task
import requests
import os
from .models import ImageResult
from django.core.files.base import ContentFile

@shared_task
def texttoimage(prompts):
    for prompt in prompts:
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
            headers={
                "authorization": f"Bearer {settings.STABILITY_API_KEY}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={
                "prompt": prompt,
                "output_format": "webp",
            },
        )

        if response.status_code == 200:
            first_letters = prompt[:5]
            result_filename = f"{first_letters}.webp"
            result_filepath = os.path.join(settings.MEDIA_ROOT, result_filename)

            with open(result_filepath, 'wb') as file:
                file.write(response.content)

            with open(result_filepath, 'rb') as file:
                image_file = ContentFile(file.read(), result_filename)
                ImageResult.objects.create(prompt=prompt, image=image_file)
            os.remove(result_filepath)
        else:
            raise Exception(str(response.json()))
    return "Task completed successfully"
