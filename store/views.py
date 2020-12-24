from django.shortcuts import render , redirect , HttpResponseRedirect
from .models import Product , Category , Customer , Order , Contact
from django.contrib.auth.hashers import make_password
from django.views import View
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth.hashers import  check_password
from .middlewares.auth import auth_middleware
from django.views.generic import TemplateView
from django.db.models import Q
import json
from django.http import JsonResponse
from .models import Setting
from django.http import HttpResponse
from . import signals


def home(request):
    signals.notification.send(sender=None, request=request, user=['Geeky','Show'])
    return HttpResponse("Thi is notification")   
# Create your views here.

class Search(TemplateView):
    template_name = "search.html"

    def get_context_data(self,**kwargs):
        # template_name = request.GET.get("template_name")
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(Q(name__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        print(kw, "...............")
        return context
    
def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(name__istartswith=request.GET.get('term'))
        names = list()
        for product in qs:
            names.append(product.name)
        return JsonResponse(names, safe=False)
    return render(request, 'templates/base.html')


class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)



#========================= SignUp =================================



class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.is_active=False
            customer.register()

            uidb64= urlsafe_base64_encode(force_bytes(customer.pk))
            domain = get_current_site(request).domain
            link=reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(customer)})

            
            activate_url='http://'+domain+link
            email_body='Hi '+customer.email + 'Please use this link to verify your account\n'+activate_url
            email_subject='Activate your acxount'
            email= EmailMessage(
                email_subject,
                email_body,
                'noreply@example.com',
                [email],
                # ['bcc@example.com'],
                # reply_to=['another@example.com'],
                # headers={'Message-ID': 'foo'},
                )
            email.send(fail_silently=False)
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message


class VerificationView(View):
    def activate(self, request, uidb64, token):
        return redirect('login')


        #====================================================
        #                                                ====
        #               L  O  G  I  N                    ====
        #                                                =====
        #=====================================================


class Login(View):
    # return_url = None
    def get(self , request):
        # Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email
                return redirect('homepage')

                # request.session['customer'] = customer.id

                # if Login.return_url:
                #     return HttpResponseRedirect(Login.return_url)
                # else:
                #     Login.return_url = None
                #     return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


#==================== CART ===========================


class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' , {'products' : products})


#====================== CHECKOUT =========




class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        # print(address, phone, customer, cart, products)

        for product in products:
            # print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
           
            order.save()
        
        request.session['cart'] = {}

        return redirect('/cart')


#===================== ORDERS ======================


class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})

def productView(request, id):
    product = Product.objects.filter(id=id)
    print(product)
    return render(request, 'prodView.html', {'product':product[0]})


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting}
    return render(request, 'about.html',context)

def contactus(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name,email,phone,desc)
        contactus = Contact(name=name, email=email, phone=phone, desc=desc)
        contactus.save()
    setting = Setting.objects.get(pk=1)
    context={'setting':setting}
    return render(request, 'contact.html', context)