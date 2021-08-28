from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from .models import Category, Product
from cart.forms import CartAddProductForm



class ProductListView(ListView):
    def get_queryset(self):
        category = None
        products = Product.objects.filter(available=True)

        category_slug = self.request.GET.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
            self.kwargs['category_slug'] = category_slug
        
        return products

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs.get('category_slug')
        # import pdb ; pdb.set_trace()
        return context

    template_name = "shop/product/list.html"
    context_object_name='products'
  

class ProductDetailView(DetailView):
    queryset = Product.objects.filter(available=True)
    template_name = "shop/product/detail.html"
    context_object_name = "product"
    form_class = CartAddProductForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['cart_add_form'] = CartAddProductForm()
        return context
  

