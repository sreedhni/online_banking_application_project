from django.contrib import admin
from .models import AccountBranches, AccountCategory, AccountType,Account,LoanDetail,LoanType

admin.site.register(AccountBranches)
admin.site.register(AccountCategory)
admin.site.register(AccountType)
admin.site.register(Account)
admin.site.register(LoanType)
admin.site.register(LoanDetail)

