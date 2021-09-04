from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, View
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from .models import Coupon
from .forms import CouponApplyForm

@method_decorator(require_POST, name='dispatch')
class CouponApply(View):
    def post(self, request,*args, **kwargs):
        now = timezone.now()
        form = CouponApplyForm(request.POST,)
        
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                request.session['coupon_id'] = coupon.id
            except ObjectDoesNotExist:
                request.session['coupon_id'] = 123 
                
        return redirect('cart:cart_detail')

   