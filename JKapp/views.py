import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
from . models import Product,Contact,Order,OrderUpdate
from math import ceil

MERCHANT_KEY='_52fJp70_t7wj49A'
mid='noUPYd58315465222312'
# Create your views here. 
def index(request):
    # products=Product.objects.all()
    # print(products)
    # n= len(products)
    # nSlides=n//4 + ceil((n/4)-(n//4))
    allProduct=[]
    productCategory=Product.objects.values('category','id')
    categorys={item['category'] for item in productCategory}
    for cat in categorys:
        prod=Product.objects.filter(category=cat)
        n= len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4))
        allProduct.append([prod,range(1,nSlides),nSlides])
    # params={'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    # allProduct=[[products,range(1,nSlides),nSlides],
    #             [products,range(1,nSlides),nSlides]]
    params={'allProduct':allProduct}
    return render(request,'shop/index.html',params)

def about(request):
    return render(request,'shop/about.html')

def contact(request):

    thank=False
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True
    return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method=="POST":
        email=request.POST.get('email','')
        order_id=request.POST.get('order_id','')
        print(email,order_id)
        try:
            order=Order.objects.filter(order_id=order_id,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=order_id)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    # response=updates
                    # print(response)
                    response=json.dumps([updates,order[0].items_json],default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request,'shop/tracker.html')

def search(request):
    return render(request,'shop/search.html')

def productView(request,myid):
    # fetch the product using id
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request,'shop/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('items_json','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address','') + " " +request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        print(name,email,address,phone,city,state,zip_code,items_json)
        order=Order(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been places")
        update.save()
        id=order.order_id
        thank=True
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        # paytm payment request
        params_dict={
            "MID": mid,
            "ORDER_ID": str(order.order_id),
            "CUST_ID": email,
            "TXN_AMOUNT": amount,
            "CHANNEL_ID": "WEB",
            "INDUSTRY_TYPE_ID": "Retail",
            "WEBSITE": "WEBSTAGING",
            "CALLBACK_URL":"http://127.0.0.1:8000/JKapp/handlerequest",
        }
        print(params_dict)
        params_dict['CHECKSUMHASH']=Checksum.generate_checksum(params_dict, MERCHANT_KEY)
        print("**************",params_dict)
        return render(request,'shop/paytm.html',{'params_dict':params_dict})

    return render(request,'shop/checkout.html')

# @csrf_exempt
# def handlerequest(request):
#     # for paytm
#     form=request.POST
#     response_dict={}
#     for i in form.keys():
#         response_dict[i]=form[i]
#         if i=='CHECKSUMHAS':
#             checkSum=form[i]
#
#     verify=checkSum.verify_checksum(response_dict,MERCHANT_KEY,checkSum)
#     if verify:
#         if response_dict['RESPCODE']=='01':
#             print("order successful")
#         else:
#             print("order was not successful" +response_dict['RESPMSG'])
#     return render(request,'shop/paymentstatus.html',{'response':response_dict})
#

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
