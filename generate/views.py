from django.shortcuts import render
from django.http import JsonResponse
from generate.task import texttoimage
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import ImageResult

@csrf_exempt
@require_POST
def trigger_task(request):
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt')
        if not prompt:
            return JsonResponse({'error': 'No prompt provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    task = texttoimage.delay(prompt)
    return JsonResponse({'task_id': task.id, 'message': 'Task has been triggered successfully'})

def check_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    response_data = {'task_status': task_result.status}

    if task_result.status == 'SUCCESS':
        prompt = task_result.result
        print(prompt)

        image_result = ImageResult.objects.filter(prompt=prompt).first()
        if image_result:
            response_data['image_url'] = image_result.image.url
        else:
            response_data['error'] = 'Image not found'

    return JsonResponse(response_data)
