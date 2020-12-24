from django.contrib import admin
from django.urls import path, include
from .views import Index , store ,Signup , VerificationView ,Login , logout , Cart , CheckOut , OrderView,Search
# from .views import Cart , CheckOut , OrderView
from .middlewares.auth import  auth_middleware
from . import views


urlpatterns = [
    path('home/',views.home),
    path('', Index.as_view(), name='homepage'),
    path('search', Search.as_view(), name='search'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('store/<int:id>', views.productView, name='ProductView'),
    path('store', store , name='store'),
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')
]