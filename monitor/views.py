from django.http import JsonResponse, HttpResponse
import time
import random

# Create your views here.
def success(req):
    return JsonResponse({'detail': 'success'}, status=200)

def error(req):
    return JsonResponse({'detail': 'error'}, status=500)

def flaky(req):
    params = req.GET
    rate = params.get('rate', 0.5)
    if random.random() < rate:
        raise JsonResponse({'detail': f'Simulated random failure (rate={rate})'}, status=500)
    return JsonResponse({'detail': 'flasky'}, status=200)

def slow(req):
    params = req.GET
    seconds = float(params.get('seconds', 1.0))
    time.sleep(seconds)
    return JsonResponse({'detail': 'slow'}, status=200)

def status_code(req):
    params = req.GET
    code = int(params.get('code', 200))
    return JsonResponse({'detail': 'status'}, status=code)