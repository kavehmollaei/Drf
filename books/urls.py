# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# ۱. ایجاد یک نمونه از روتر
router = DefaultRouter()

# ۲. ثبت نام ویوست در روتر (پیشوند آدرس را مشخص می‌کنیم)
router.register(prefix=r'books', viewset=BookViewSet, basename='book')
# برای کتاب ها آدرس بساز
# ۳. اضافه کردن مسیرهای روتر به لیست کلی URLs
urlpatterns = [
    path('api/', include(router.urls)),
]