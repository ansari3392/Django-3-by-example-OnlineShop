import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView, View
from django.conf import settings
from orders.models import Order

#instantiate braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

class PaymentProcessView(View):
    def post(self, request):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.get_total_cost()
        #retrieve nonce
        nonce = self.request.POST.get('payment_method_nonce', None)
        #create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce, 
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            #mark the order as paid
            order.paid = True
            #store the unique transaction id 
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')

    def get(self, request):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.get_total_cost()
        #generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order':order, 'client_token':client_token})



class PaymentDoneView(TemplateView):
    template_name = 'payment/done.html'


class PaymentCanceledView(TemplateView):
    template_name = 'payment/canceled.html'