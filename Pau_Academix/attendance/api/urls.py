from rest_framework.routers import DefaultRouter
from attendance.api.views import StartAttendanceAPIView, ScanQRCodeAPIView, CleanupAttendanceAPIView
from django.urls import path

router = DefaultRouter()

urlpatterns = [
    path('start-attendance/', StartAttendanceAPIView.as_view(), name='start-attendance'),
    path('scan-qrcode/',ScanQRCodeAPIView.as_view(), name='scan-qrcode'),
    path('cleanup-attendance/', CleanupAttendanceAPIView.as_view(), name='cleanup-attendance'),
    ]

urlpatterns += router.urls