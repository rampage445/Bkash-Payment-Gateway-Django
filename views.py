from django.shortcuts import render,redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse,Http404
import requests,json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Transaction
from django.shortcuts import get_list_or_404
from django.contrib import messages

def query_payment(paymentID,authorization,app_key):
    url = f"https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/query/{paymentID}"

    headers = {
        "accept": "application/json",
        "Authorization": authorization,
        "X-APP-Key": app_key
    }
    response = requests.get(url, headers=headers)
    return not(json.loads(response.text)['message'] == "Unauthorized")

@login_required
def get_token(request):
    url = settings.BKASH_TOKEN_URL

    payload = {
        "app_key": settings.BKASH_APP_KEY,
        "app_secret": settings.BKASH_SECRET_KEY
    }
    headers = {
        "accept": "application/json",
        "username": settings.BKASH_USERNAME,
        "password": settings.BKASH_PASSWORD,
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response = json.loads(response.text)
    request.session['id_token'] = response['id_token']
    return redirect(reverse('createpayment'))

@transaction.atomic
def execute_payment(request,paymentid):
    url = settings.BKASH_EXECUTE_PAYMENT_URL
    payload = { "paymentID": paymentid }
    headers = {
        "accept": "application/json",
        "Authorization": request.session.get('id_token',''),
        "X-APP-Key": settings.BKASH_APP_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_dict = json.loads(response.text)
    if response_dict['statusCode'] == "0000":
        obj = Transaction.objects.create(user_id=request.user.user_id,paymentID=response_dict['paymentID'],
                                   transactionStatus=response_dict['transactionStatus'],statusCode=response_dict['statusCode'],trxID=response_dict['trxID'])
        request.user.total_credit += 10 #if payment is done, user gets some credit
        request.user.save()
        obj.save()
        print("Payment is done!") #payment complete
    else:
        print("Payment failed!")
    return redirect(reverse('Home')) #go to home

def callback(request):
    done = request.GET.get('status','failure')=="success"
    if done:
        #if query_payment(request.GET.get('paymentID',''),request.session.get('id_token',''),settings.BKASH_APP_KEY):
        return redirect(reverse('executepayment',kwargs={'paymentid':request.GET.get('paymentID','')})) #redirects to execute payment
    return HttpResponse(status=404)
    

def create_payment(request):
    payload = {
        "mode": "0011",
        "payerReference": "REF",
        "callbackURL": "http://127.0.0.1:8000/bkash/payment/callback", #calls the callback function above
        "amount": 500,
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": "abc"
    }
    headers = {
        "accept": "application/json",
        "Authorization": request.session.get('id_token',''),
        "X-APP-Key": settings.BKASH_APP_KEY,
        "content-type": "application/json"
    }
    response = requests.post(settings.BKASH_CREATE_PAYMENT_URL, json=payload, headers=headers)
    return redirect(json.loads(response.text)['bkashURL'])



