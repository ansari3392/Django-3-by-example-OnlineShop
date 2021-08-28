from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
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
            order = form.save()
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


class AdminOrderDetailView(DetailView):
    def get_context_data(self, **kwargs):
        context = super(AdminOrderDetail, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, id=order_id)
        return context

    template_name = 'admin/orders/order/detail.html'
