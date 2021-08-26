from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


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
            return render(request, 'orders/order/created.html', {'order':order})

    def get(elf, request):
        cart = Cart(self.request)
        form = OrderCreateForm()
        return render(request, 'orders/order/created.html', {'cart':cart, 'form':form})