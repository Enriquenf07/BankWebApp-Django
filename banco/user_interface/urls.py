from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("conta", views.AccountView.as_view(), name='account'),
    path('pix', views.TransactionView.as_view(), name='transaction'),
    path('success', views.SuccessView.as_view(), name='success'),
    path('pix-area', views.TransferAreaView.as_view(), name='transfer_area')
]
