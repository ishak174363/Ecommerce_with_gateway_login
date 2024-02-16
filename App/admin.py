from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']
    def product(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_id','razorpay_payment_status','paid']

@admin.register(OrderPlaced)
class OrderPlaceModeldAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']
    def product(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    def customer(self,obj):
        link=reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    def payment(self,obj):
        link=reverse("admin:app_payment_change",args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.amount)


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']
    def product(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

#unregister the group model from admin
admin.site.unregister(Group)