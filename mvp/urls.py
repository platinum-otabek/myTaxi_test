from django.urls import path

from .views import ListCreateDriverView, GetUpdateDeletDriverView, ListCreateClientView, GetUpdateDeleteClientView
from .views.orderView import ListCreateOrderView, UpdateOrderStatus, OrderClientDetail

urlpatterns = [
    # related Driver api CRUD
    path('driver/', ListCreateDriverView.as_view()),
    path('driver/<int:pk>/', GetUpdateDeletDriverView.as_view()),
    # related Client api CRUD
    path('client/', ListCreateClientView.as_view()),
    path('client/<int:pk>/', GetUpdateDeleteClientView.as_view()),
    # related Order api
    path('orders/', ListCreateOrderView.as_view()),  # create adn list orders
    path('orders/<int:pk>/', UpdateOrderStatus.as_view()),  # update status
    path('orders/clients/<int:pk>/', OrderClientDetail.as_view())  # order_client detail
]
