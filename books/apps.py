from django.apps import AppConfig





class BooksConfig(AppConfig):
    name = 'books'
    
    def ready(self):
        from django.core.signals import request_finished
        from books.signals import my_callback
        request_finished.connect(receiver=my_callback,dispatch_uid="request_finished_once")
        
        
