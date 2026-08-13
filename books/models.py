
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    author = models.CharField(max_length=100)
    price = models.IntegerField(default=1000)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE,default=1,null=True)

    # ۲. رابطه چند‌به‌چند (ManyToManyField) با نویسندگان [۵۷]
    contributors = models.ManyToManyField("Contributor")

    # ۳. رابطه یک‌به‌یک (OneToOneField) برای جزئیات فنی [۶۳، ۱۶۶]
    metadata = models.OneToOneField("BookMetadata", on_delete=models.CASCADE, null=True, blank=True)

    def __string__(self):
        return self.title



class Publisher(models.Model):
    """مدلی برای اطلاعات ناشر [۴۴]"""
    name = models.CharField(max_length=50, help_text="نام ناشر")
    email = models.EmailField(help_text="email",default="asd@yahoo.com")
    def __str__(self):
        return self.name

class Contributor(models.Model):
    """مدلی برای اطلاعات نویسندگان و همکاران [۴۹]"""
    first_names = models.CharField(max_length=50)
    last_names = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_names} {self.last_names}"

class BookMetadata(models.Model):
    """اطلاعات تکمیلی یک‌به‌یک برای کتاب [۱۶۶]"""
    summary = models.TextField(help_text="خلاصه اختصاصی کتاب")
    page_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.summary


import factory
class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    # تولید عنوان تصادفی با استفاده از فیلترهای داخلی
    title = factory.Faker('sentence', nb_words=10)
    author = factory.Faker('name')
    price = factory.Faker('random_int', min=50000, max=500000)
    