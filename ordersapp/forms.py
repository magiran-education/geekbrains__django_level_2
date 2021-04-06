from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field_name.widget.attrs['class'] = 'form-control'


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self):
        super(OrderItemsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field_name.widget.attrs['class'] = 'form-control'
