from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customers'),
    path('create_order/<str:pk>/',views.createOrder, name = 'create_order'),
    path('update_order/<str:pk>/',views.updateOrder, name = 'update_order'),
    path('remove_order/<str:pk>/',views.removeOrder, name = 'remove_order'),
]