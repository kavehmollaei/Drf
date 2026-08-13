from rest_framework import serializers
from .models import Book,Publisher,Contributor

# class BookSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = Book
        # fields = '__all__'
# serializers.py
# class BookListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ('id', 'title') # فقط عنوان در لیست نمایش داده شود

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # تمام جزئیات در نمایش تکی


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'email']


class ContributorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["first_names","last_names"]
        

# سریالایزر اصلی کتاب
class BookSerializer(serializers.ModelSerializer):
    # استفاده از سریالایزر تودرتو برای نمایش جزئیات ناشر [۱۷۳، ۱۸۵]
    publisher = PublisherSerializer(read_only=True)
    # contributors = ContributorsSerializers(many=True)
    is_expensive = serializers.SerializerMethodField()
    # contributors = serializers.SerializerMethodField()
    display_contributors = serializers.SerializerMethodField()
    class Meta:
        model = Book
        read_only_fields=("id",) 
        fields = ['id', 'title', 'author', 'price', 'publisher','display_contributors','contributors','is_expensive']
        extra_kwargs = {'contributors':{'write_only':True},'price':{'required':True,'error_messages':{'required':"fffffff",'invalid':'ftttt'}}}
    
    
    def get_is_expensive(self, obj):
        """
        این متد شیء مدل فعلی (obj) را می‌گیرد و محاسبات را انجام می‌دهد [۱۳۱].
        """
        # منطق پایتونی شما در اینجا قرار می‌گیرد
        if obj.price > 700:
            return True
        return False
    
    def get_display_contributors(self,obj):
        contributors=obj.contributors.all()
          # ترکیب نام و نام خانوادگی برای هر همکار [۵، ۴۹]
        return [f"{c.first_names} and {c.last_names}" for c in contributors]
    
    
    def validate_price(self,value):
        if value <= 500:
            raise serializers.ValidationError("price must be upper 500")
        return value
        
    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        book_title=validated_data.pop("title")
        contributors_data = validated_data.pop("contributors", [])
        
        if "test" in book_title:
            validated_data.update({"title":None})
            book=Book.objects.create(**validated_data)
            if contributors_data:
                book.contributors.set(contributors_data)
            return book
        
        validated_data["title"] = book_title
        return super().create(validated_data)
    
    
    
    def update(self, instance, validated_data):
        # ۱. به‌روزرسانی فیلدهای معمولی (اگر داده جدید نبود، از قبلی استفاده کن)
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        
        # ۲. مدیریت روابط چند‌به‌چند (M2M)
        # اگر در داده‌ها فیلد contributors وجود داشت، آن را جایگزین کن
        if 'contributors' in validated_data:
            contributors = validated_data.pop('contributors')
            instance.contributors.set(contributors)

        # ۳. ذخیره نهایی در دیتابیس
        instance.save()
        
        # ۴. بازگرداندن شیء به‌روز شده برای نمایش در خروجی [۱۸۵]
        return instance
    
    # def create(self, validated_data):
    #     print(validated_data)
    #     contributors_data = validated_data.pop('contributors', [])
    #     book = Book.objects.create(**validated_data)
    #     if contributors_data:
    #         book.contributors.set(contributors_data)
    #     return book
    