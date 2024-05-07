# urls.py
from django.urls import path
from .views import AccountStatusChangeView,AccountListView,LoanApplicationListView,LoanStatusChangeView

urlpatterns = [
    path('account-status-change/', AccountStatusChangeView.as_view(), name='account-status-change'),
    path('accounts/', AccountListView.as_view(), name='account-list'),
    path('loan-applications/', LoanApplicationListView.as_view(), name='loan_applications_list'),
    path('loan-status-change/', LoanStatusChangeView.as_view(), name='loan-status-change'),
]

