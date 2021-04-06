from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from basketapp.models import Basket
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemsForm

from django.contrib.auth.mixins import LoginRequiredMixin


class OrderList(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(LoginRequiredMixin, CreateView):
    print('======= 1 =======')
    model = Order
    fields = []
    context_object_name = 'object'
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        print('======= 2 =======')
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            print('======= 3 =======')
            formset = OrderFormSet(self.request.POST)
        else:
            print('======= 4 =======')
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                print('======= 5 =======')
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                basket_items.delete()
            else:
                print('======= 6 =======')
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        print('======= 7 =======')
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                print('======= 8 =======')
                orderitems.instance = self.object
                orderitems.save()

            # удаляем пустой заказ
            if self.object.get_total_cost() == 0:
                print('======= 9 =======')
                self.object.delete()

            return super(OrderItemsCreate, self).form_valid(form)







def order_forming_complete():
    pass


class OrderRead(ListView):
    pass


class OrderItemsUpdate(ListView):
    pass


class OrderDelete(ListView):
    pass
