from django.urls import path
from .views import (
    success, error, flaky, slow, status_code
)

urlpatterns = [
    path('api/success', success, name='success'),
    path('api/error', error, name='error'),
    path('api/flaky', flaky, name='flaky'),
    path('api/slow', slow, name='slow'),
    path('api/status', status_code, name='status-code')
]