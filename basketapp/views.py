from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from mainapp.models import Product
from basketapp.models import Basket

from django.views.generic import DeleteView, CreateView


@login_required
def basket_add(request, product_id=None):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity = 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def basket_delete(request, id=None):
#     basket = Basket.objects.get(id=id)
#     basket.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class BasketDelete(LoginRequiredMixin, DeleteView):
    model = Basket
    success_url = reverse_lazy('auth:profile')

    # наверно, не самая лучшая идея в GET запускать POST метод
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})
