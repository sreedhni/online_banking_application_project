from django.urls import path
from Customer import views


urlpatterns = [path('account-application/',views.OpenAccountView.as_view(),name="open-account"),
 path('allaccountdetails/', views.AccountListView.as_view(), name='all-account'),   

 path('accounts/<int:pk>/edit/', views.EditAccountView.as_view(), name='edit_account'),   
 path('my-account/', views.MyAccount.as_view(), name='my-account'),
 path('deposit/', views.DepositeAmountView.as_view(), name='transaction-list'),   
 path('loan-apply/', views.LoanApplyView.as_view(), name='loan_apply'),
 path('withdraw/', views.WithdrawAmountView.as_view(), name='withdraw'),  
 path('loan/<int:pk>/', views.LoanDetailView.as_view(), name='loan-detail'), 
 path('repayment/', views.LoanRepaymentView.as_view(), name='loan-repayment'),

        
]
