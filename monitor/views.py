from django.http import JsonResponse, HttpResponse
import time
import random
import logging

logger = logging.getLogger(__name__)

def success(request):
    logger.info("success endpoint hit", extra={"path": request.path, "status": 200})
    return JsonResponse({'detail': 'success'}, status=200)

def error(request):
    logger.error("error endpoint hit, raising exception", extra={"path": request.path, "status": 500})
    raise RuntimeError("Simulated failure from /api/error/")

def flaky(request):
    params = request.GET
    rate = params.get('rate', 0)
    if random.random() < rate:
        logger.error("flaky endpoint failed", extra={"path": request.path, "status": 500, "rate": rate})
        raise JsonResponse({'detail': f'Simulated random failure (rate={rate})'}, status=500)
    logger.info("flaky endpoint succeeded", extra={"path": request.path, "status": 200, "rate": rate})
    return JsonResponse({"status": "ok", "rate": rate})

def slow(request):
    params = request.GET
    seconds = float(params.get('seconds', 1.0))
    start = time.monotonic()
    time.sleep(seconds)
    duration_ms = round((time.monotonic() - start) * 1000)
    logger.info("slow endpoint finished", extra={"path": request.path, "status": 200, "duration_ms": duration_ms})
    return JsonResponse({"status": "ok", "slept_seconds": seconds})

def status_code(request):
    params = request.GET
    code = int(params.get('code', 200))
    if not 200 <= code <= 599:
        logger.warning("status invalid code", extra={"path": request.path, "status": 400, "requested": code})
        return JsonResponse({"error": "code must be between 200 and 599"}, status=400)

    extra = {"path": request.path, "status": code}
    if code >= 500:
        logger.error("status endpoint returning server error", extra=extra)
    elif code >= 400:
        logger.warning("status endpoint returning client error", extra=extra)
    else:
        logger.info("status endpoint returning success", extra=extra)
    return JsonResponse({"status": code}, status=code)