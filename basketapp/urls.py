from django.urls import path

from basketapp.views import basket_add, basket_edit
from .views import BasketDelete

app_name = 'basketapp'

urlpatterns = [
    path('basket-add/<int:product_id>/', basket_add, name='basket_add'),
    # path('basket-delete/<int:id>/', basket_delete, name='basket_delete'),
    path('basket-delete/<int:pk>/', BasketDelete.as_view(), name='basket_delete'),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
