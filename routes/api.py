from django.urls import path
from apps.products.api.views import *
from apps.stores.api.views import *
from apps.orders.api.views import *

urlpatterns = [
    path('drugs/', DrugListView.as_view(), name='drugs'),
    path('drugs/<int:pk>/', DrugDetailView.as_view()),
    path('category/', CategoryListView.as_view()),

    path('stores/', StoreListView.as_view()),
    path('regions/', RegionListView.as_view()),

    path('order/', OrderListView.as_view(), name='order'),
    path('add_order/', add_order, name='add_order')
]






















































































































