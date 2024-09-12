from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from paymentapp.models import StripePayment
from django.utils import timezone


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentIntentView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # amount in cents
            currency='usd',
            payment_method_types=[
                'card',            # Card payments
                # 'netbanking',      # Net banking
                # 'upi',             # UPI
                # 'upi_qr',          # UPI QR code
                # Add other payment methods as needed
            ],
        )
        return Response({'client_secret': intent.client_secret})



class ConfirmPaymentView(APIView):
    def post(self, request):
        payment_intent_id = request.data.get('payment_intent_id')
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            print(intent.status,'*********************************')
            if intent.status == 'succeeded':
                # Save payment details in the database
                StripePayment.objects.create(
                    customer=request.user,
                    stripe_charge_id=intent.id,
                    amount=intent.amount / 100,
                    status='succeeded',
                    created_at = timezone.now(),
                )
                return Response({'status': 'success'})
            else:
                return Response({'status': 'failed'})
        except stripe.error.StripeError as e:
            return Response({'error': str(e)})



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Update payment status in the database
    
    return JsonResponse({'status': 'success'})