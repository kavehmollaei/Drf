from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Book
# from .serializers import BookSerializer
from .serializers import BookDetailSerializer,BookSerializer

class BookViewSet(ModelViewSet):
    # queryset = Book.objects.all()
    queryset = Book.objects.prefetch_related('contributors').all()
    serializer_class = BookSerializer
    
    # def get_queryset(self):
    #     user=self.request.user
    #     if user.is_staff:
    #         return Book.objects.all()
        
    #       # در غیر این صورت، فقط کتاب‌های متعلق به این کاربر را برگردان
    #     return Book.objects.filter(author=user)
    
    
    def create(self, request, *args, **kwargs):
        print("sdddddddddd")
        return super().create(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Book.objects.all()
        search_term = self.request.query_params.get('q')
        if search_term:
        # فیلتر کردن کتاب‌هایی که عنوانشان شامل این کلمه است [۹۲، ۱۶۳]
            queryset = queryset.filter(title__icontains=search_term) 
        
        return queryset

    def get_serializer_class(self):
            #* بررسی اکشن جاری با استفاده از ویژگی self.action [۷، ۸]

            if self.action == 'list' or self.action == 'create' or self.action == 'update' or self.action =='retrieve':
                return BookSerializer
            
            # برای سایر اکشن‌ها مثل retrieve یا create از سریالایزر کامل استفاده کن
            return BookDetailSerializer

    
    def list(self, request, *args, **kwargs):

        print(self)
        queryset=self.get_queryset()
        count_of_books=queryset.count()
        serializer_data=self.get_serializer(queryset,many=True)
        data=serializer_data.data
        
        custom_data={"count":count_of_books,"data":data}
        return Response(custom_data)    
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest_books = Book.objects.all().order_by('-id')[:3]
        serializer = self.get_serializer(latest_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=["get"],url_path="cheapBooks")
    def cheap_books(self,request):
        books = Book.objects.filter(price__gt=2000)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
        
    @action(detail=True,methods=["post"])
    def apply_discount(self, request, pk=None):
    # ۱. واکشی آبجکت کتاب بر اساس شناسه موجود در آدرس [۱۸۵]
        book = self.get_object()
        
        # ۲. دریافت درصد تخفیف از بدنه درخواست (مثلاً {"percent": 20})
        discount_percent = request.data.get('percent')
        
        if discount_percent is None:
            return Response({'error': 'لطفاً درصد تخفیف را وارد کنید.'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            percent = int(discount_percent)
            if not (0 <= percent <= 100):
                raise ValueError
        except ValueError:
            return Response({'error': 'درصد معتبر نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        # ۳. محاسبه قیمت جدید و تبدیل به عدد صحیح (Integer) [۱۷۹]
        discount_amount = (book.price * percent) // 100
        book.price -= discount_amount
        
        # ۴. ذخیره تغییرات در دیتابیس [۱۵۲، ۱۵۳]
        book.save()
        
        return Response({
            'status': 'تخفیف با موفقیت اعمال شد.',
            'old_price': book.price + discount_amount,
            'new_price': book.price,
            'discount_applied': f'{percent}%'
        }, status=status.HTTP_200_OK)
        
        
# add comment