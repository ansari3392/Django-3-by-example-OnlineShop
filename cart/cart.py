from decimal import Decimal 
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon



class Cart(object):
    def __init__(self, request):
        # initialize the cart
        self.session = request.session   #current session to be accessible to  other methods
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        #store current applied coupon
        self.coupon_id = self.session.get('coupon_id')
        

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = { 'quantity':0, 'price':str(product.price)}    
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()


    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None 

    
    def get_discount(self):
        if self.coupon:
           return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()










#  rest frame work #
#  from rest_framework.validators import ValidationError

# from product_pack.models import ProductPack

# CART_SESSION_ID = "cart"


# class SessionCart:
#     def _init_(self, request):
#         """
#             get the session of user if not exists it will create one
#         """
#         self.session = request.session
#         cart = self.session.get(CART_SESSION_ID)
#         if not cart:
#             cart = self.session[CART_SESSION_ID] = {}
#         self.cart = cart

#     def _iter_(self):
#         product_skus = self.cart.keys()
#         products = ProductPack.objects.filter(sku__in=product_skus)
#         cart = self.cart.copy()
#         for product in products:
#             cart[product.sku]['product'] = product

#         for item in cart.values():
#             yield item

#     def add(self, product_pack, quantity):
#         """
#             it will receive 
#         """
#         product_pack_sku = str(product_pack.sku)
#         if product_pack_sku not in self.cart:
#             self.cart[product_pack_sku] = {'quantity': int(quantity)}
#         else:
#             self.cart[product_pack_sku]['quantity'] += int(quantity)
#         self.save()

#     def add_quantity_by_one(self, product_pack):
#         product_sku = str(product_pack.sku)
#         if product_sku not in self.cart:
#             raise ValidationError(detail={"message": "product not found"})
#         self.cart[product_sku]['quantity'] += 1
#         self.save()

#     def subtract(self, product):
#         product_sku = str(product.sku)
#         if product_sku not in self.cart:
#             raise ValidationError(detail={"message": "product not found"})
#         self.cart[product_sku]['quantity'] -= 1
#         self.save()

#     def remove(self, product):
#         product_sku = str(product.sku)
#         if product_sku not in self.cart:
#             raise ValidationError(detail={"message": "product not found"})
#         del self.cart[product_sku]
#         self.save()

#     def get_cart_items(self):
#         item_list = []
#         for sku, quantity in self.cart.items():
#             item_list.append({sku: quantity})
#         return item_list

#     def save(self):
#         self.session.modified = True

#     def clear(self):
#         self.session[CART_SESSION_ID] = {}
#         self.save()


