from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get-token/',views.get_token,name='gettoken'),
    path('create-payment/',views.create_payment,name='createpayment'),
    path('callback/',views.callback,name='callback'),
    path('execute-payment/<str:paymentid>/',views.execute_payment,name='executepayment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)