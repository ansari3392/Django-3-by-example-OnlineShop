from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView, View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created


class OrderCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def post(self, request):
        form = OrderCreateForm(request.POST,)
        cart = Cart(self.request)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                        price=item['price'], quantity=item['quantity'])
            cart.clear()
            #launch asynch task
            order_created.delay(order.id)
            #set order in session
            self.request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    def get(self, request):
        cart = Cart(self.request)
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})



@method_decorator(staff_member_required, name='dispatch')
class AdminOrderDetailView(View):
    def get(self, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        return render(self.request, 'admin/orders/order/detail.html', {'order': order})


# @method_decorator(staff_member_required, name='dispatch')
# class AdminOrderPdf(View):
#     def get(self, *args, **kwargs):
#         order_id = self.kwargs.get('order_id')
#         order = get_object_or_404(Order, id=order_id)
#         html = render_to_string('orders/order/pdf.html', {'order': order})
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#         weasyprint.HTML(string=html).write_pdf(response,
#         stylesheets=[weasyprint.CSS(
#             settings.STATIC_ROOT + 'css/pdf.css')])
#         return response

    
