from django.shortcuts import render,redirect
from django.views import View
from urllib import request
from django.db.models import Count
from .models import Product, Customer, Cart
from .forms import CustomRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

class CategoryView(View):
    def get(self, request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'app/category.html',locals())

class CategoryTitle(View):
    def get(self, request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,'app/category.html',locals())

class ProductDetail(View):
    def get(self, request,pk):
        product=Product.objects.get(id=pk)
        return render(request,'app/productdetail.html',locals())   


class CustomerRegistrationView(View):
    def get(self, request):
        form=CustomRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self, request):
        form=CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations!! Registered Successfully')
        else:
            messages.warning(request,'Failed to Register')   
        return render(request, 'app/customerregistration.html',locals())

class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            zipcode=form.cleaned_data['zipcode']
            state=form.cleaned_data['state']

            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,zipcode=zipcode,state=state)
            reg.save()
            messages.success(request,'Congratulations!! Profile Saved Successfully')
        else:
            messages.warning(request,'Invalid Data Entered')

        return render(request, 'app/profile.html',locals())


def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.zipcode=form.cleaned_data['zipcode']
            add.state=form.cleaned_data['state']
            add.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        else:
            messages.warning(request,'Invalid Data Entered')
        return redirect('address')


#checkout
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount+=value
        totalamount=famount+50
        return render(request, 'app/checkout.html',locals())


#add to cart
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('product_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/showcart')


#show cart
def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount+=value
    totalamount=amount+50        #50 is the shipping charge 
    return render(request, 'app/addtocart.html',locals())


#plus cart
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discounted_price
            amount+=value
        totalamount=amount+50
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

#minus cart
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1      # Decrement quantity
        
        if c.quantity <= 0:
            c.delete()      # If quantity becomes less than or equal to 0, remove the item from the cart
        else:
            c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0     # Calculate the total amount
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        
        total_amount = amount + 50
        data = {
            'quantity': c.quantity if hasattr(c, 'quantity') else 0,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)

#remove cart
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        cart_items = Cart.objects.filter(product=prod_id, user=request.user)
        if cart_items.exists():
            c = cart_items.first()
            c.delete()
            user=request.user
            cart=Cart.objects.filter(user=user)
            amount=0
            for p in cart:
                value=p.quantity * p.product.discounted_price
                amount+=value
            totalamount=amount+50
            data={
                'amount':amount,
                'totalamount':totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item not found'})