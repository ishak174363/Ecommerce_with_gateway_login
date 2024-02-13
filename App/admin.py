from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_id','razorpay_payment_status','paid']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']