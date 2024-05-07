from django.db import models

    
    



class AccountCategory(models.Model):
    """
    Model representing different categories of accounts.
    """

    CHOICES = (
        ('Personal', 'Personal'),
        ('NRI', 'NRI'),
        ('Business', 'Business'),
    )
    account_category = models.CharField(max_length=20, choices=CHOICES)
    
    def __str__(self):
        return self.account_category

    
class AccountBranches(models.Model):
    """
    Model representing different branches of accounts.
    """

    state = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    branch_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.branch_name

    
class AccountType(models.Model):
    """
    Model representing different types of accounts.
    """

    category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=200)
    
    def __str__(self):
        return self.account_type
    
    def minimum_age(self):
        if self.account_type:
            return self.account_type.minimum_age
        return None
    
     
     

    


    
class Account(models.Model):
    """
    Model representing individual accounts.
    """

    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)#celesta
    minimum_balance = models.PositiveIntegerField()
    minimum_age = models.PositiveIntegerField()
    maximum_transaction_amount_per_day = models.PositiveIntegerField()
    eligibility = models.CharField(max_length=200)
    account_details = models.TextField(max_length=500)

    def __str__(self):
        return self.account_name
    
    def account_category(self):
        return self.account_type.account_type
    
    def category(self):
        return self.account_type.account_type.account_category
    

class LoanType(models.Model):
    """
    Model representing different types of loans.
    """

    loan_category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=50)

    def __str__(self):
        return self.loan_type
    
    def loan_category(self):
        return self.loan_category.account_type

    

class LoanDetail(models.Model):
    """
    Model representing details of different loan options.
    """

    option = (
        ('home document', 'Home Document'),
        ('property document', 'Property Document'),
        ('salary certificate', 'Salary Certificate'),
        ("no document needed", "No Document Needed")
    )
    loan_type = models.ForeignKey(LoanType, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  
    maximum_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    year = models.PositiveIntegerField() 
    required_document = models.CharField(max_length=20, choices=option)
    how_apply = models.CharField(max_length=200)
    
    # def monthly_payment(self):
    #     return 
    def __str__(self):
        return f"{self.loan_type} - {self.maximum_amount}"
