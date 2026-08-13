from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book,Publisher,Contributor,BookMetadata

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author') # نمایش ستون‌های عنوان و نویسنده [3]
    search_fields = ('title',) # اضافه کردن قابلیت جستجو [4]

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("first_names","last_names")
    
    
@admin.register(BookMetadata)
class BookMetadataAdmin(admin.ModelAdmin):
    list_display = ("summary","page_count")
    