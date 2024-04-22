"""API URL Configuration"""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import TransactionListView, SetCardTransactionDataViewSet

router = DefaultRouter()

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^set-card-transactions-data/$', SetCardTransactionDataViewSet.as_view()),
    re_path(r'^get-transactions/$', TransactionListView.as_view())
]
