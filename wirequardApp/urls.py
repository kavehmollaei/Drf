# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path('servers/', ServerListCreateView.as_view(), name='server-list-create'),
    path('servers/<int:pk>/config/', ServerConfigView.as_view(), name='server-config'),
    path('servers/<int:server_id>/clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/config/', ClientConfigView.as_view(), name='client-config'),
    path('clients/<int:pk>/config/download/',  ClientConfigDownloadView.as_view(), name='client-config'),
]
# ۱. ایجاد یک نمونه از روتر
# router = DefaultRouter()

# ۲. ثبت نام ویوست در روتر (پیشوند آدرس را مشخص می‌کنیم)
# router.register(prefix=r'books', viewset=BookViewSet, basename='book')
# برای کتاب ها آدرس بساز
# ۳. اضافه کردن مسیرهای روتر به لیست کلی URLs
# urlpatterns = [
#     path('api/', include(router.urls)),
# ]