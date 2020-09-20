from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('about',views.about,name='AboutUs'),
    path('contact',views.contact,name='ContactUs'),
    path('tracker',views.tracker,name='Tracking'),
    path('search',views.search,name='Search'),
    path('products/<int:myid>',views.productView,name='productView'),
    path('checkout',views.checkout,name='CheckOut'),
    # path('payment',views.payment,name='payment'),
    path('handlerequest',views.handlerequest,name='HandleRequest'),

]
 