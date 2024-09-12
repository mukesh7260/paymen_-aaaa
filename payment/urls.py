
from django.contrib import admin
from django.urls import path
from paymentapp import views 
from paymentapp.views import stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-payment-intent/', views.CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    # path('confirm-payment/', views.ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('strip_webhook/',stripe_webhook, name='strip_webhooks'),
]
