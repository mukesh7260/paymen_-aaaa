from django.contrib import admin
from paymentapp.models import StripePayment 

@admin.register(StripePayment)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = ['id','customer','stripe_charge_id','amount','status','created_at']
    

