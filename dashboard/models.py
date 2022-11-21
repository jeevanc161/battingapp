import os
import time
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from uuid import uuid4


def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.username:
        filename = '{}_{}.{}'.format(instance.username, time.strftime("%Y/%m/%d") , ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class User(AbstractUser):
    '''
     Custom user model and define custom fields for the model
    '''

    middle_name             = models.CharField(max_length= 20 , null=True, blank=True)
    account_created_date    = models.DateTimeField(auto_now_add=True , null=True, blank=True)
    account_created_time    = models.TimeField(auto_now_add=True , null=True, blank=True)
    phone_number            = models.CharField(max_length =25 , unique=True)
    country                 = CountryField(null=True, blank=True)
    city                    = models.CharField(max_length=50 , null=True, blank=True)
    dob                     = models.DateField(max_length=8 , null=True, blank=True)
    status                  = models.BooleanField(default = False)
    login_status            = models.BooleanField(default = False)
    is_betting_user         = models.BooleanField(default = False)
    
    # Document related fields
    profile_picture         = models.ImageField(upload_to=path_and_rename ,null=True , blank=True)
    aadhar_card             = models.FileField(upload_to ='uploads/',null=True , blank=True)
    pen_card                = models.FileField(upload_to ='uploads/',null=True , blank=True)
    bank_passbook           = models.FileField(upload_to ='uploads/',null=True , blank=True)

    # bank account details related fields
    account_holder_name    = models.CharField(max_length = 50 ,null=True , blank=True)
    bank_account_number     = models.CharField(max_length=50 ,null=True , blank=True)
    bank_name               = models.CharField(max_length = 250 ,null=True , blank=True)
    ifsc_code               = models.CharField(max_length = 250 ,null=True , blank=True)
    wallet_amount           = models.FloatField(default = 0.0)
    total_bonus_amount      = models.FloatField(default = 0.0)
    account_opening_bonus   = models.FloatField(default = 0.0)


    def __str__(self):
        return self.username


class Assets(models.Model):
    '''
        Model class for managing the Asserts
    '''

    name                    = models.CharField(max_length=250 )
    icon                    = models.FileField(upload_to ='icon/',null=True , blank=True)
    current_market_price    = models.FloatField(null=True , blank=True)
    yesterday_price         = models.FloatField(null=True , blank=True)
    returns                 = models.FloatField(null=True , blank=True)
    increament_decreament   = models.FloatField(null= True , blank = True)
    active                  = models.BooleanField(default = False)


    def __str__(self):
        return self.name


DEPOSIT_STATUS = [ # pending , success decline
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),
            ] 

class DepositHistory(models.Model):
    '''
        Model class for managing the Deposit History of the User
    '''

    user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
    transaction_date        = models.DateTimeField(auto_now_add=True)
    transaction_time        = models.TimeField(auto_now_add=True )
    amount                  = models.FloatField(default=0.0)
    bonus_amount            = models.FloatField()
    payment_id              = models.CharField(max_length= 250)
    payment_mode            = models.CharField(max_length=250)
    payment_source          = models.CharField(max_length = 250)
    status                  = models.IntegerField(choices = DEPOSIT_STATUS , default = 0)

    def __str__(self):
        return self.user_id.username

OFFER_STATUS = [
                (1, 'Active'),
                (0, 'Inactive')
            ]

class DepositOffers(models.Model):
    '''
        Model class for managing the Deposit Offer
    '''

    name                    = models.CharField(max_length=250)
    deposit_amount          = models.FloatField(default=0.0)
    bonus_amount            = models.FloatField(default= 0.0)
    date                    = models.DateTimeField(auto_now_add = True)
    status                  = models.SmallIntegerField(choices = OFFER_STATUS)

    def __str__(self):
        return self.name

WITHDROW_HISTORY_STATUS = [
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),
            ]
class WithdrawHistory(models.Model):
    '''
        Model class for managing the Deposit Offer
    '''

    user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
    transaction_date        = models.DateTimeField(auto_now_add=True)
    transaction_time        = models.TimeField(auto_now_add = True)
    amount                  = models.FloatField(default = 0.0)
    payment_id              = models.CharField(max_length= 250)
    payment_mode            = models.CharField(max_length=250)
    payment_source          = models.CharField(max_length = 250)
    status                  = models.IntegerField(choices = WITHDROW_HISTORY_STATUS , default = 0)
    remarks                 = models.TextField()

    def __str__(self):
        return self.user_id.username


WITHDROW_STATUS = [
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),

            ]

class WithdrawRequest(models.Model):
    '''
        Model class for managing the Withdraw Request
    '''

    user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
    request_amount          = models.FloatField(default=0.0)
    date_time               = models.DateTimeField(auto_now_add= True)
    status                  = models.SmallIntegerField(choices= WITHDROW_STATUS, default = 0)

    def __str__(self):
        return self.user_id.username

TRAD_STATUS = [
                (0, 'Pending'), 
                (1, 'Success'),
                (2 ,'Decline'),
            ]
 
class TradHistory(models.Model):
    '''
        Model class for managing the Trad History
    '''

    user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
    assert_id               = models.ForeignKey(Assets , on_delete=models.CASCADE)
    time                    = models.TimeField(auto_now_add = True)
    date                    = models.DateTimeField(auto_now_add = True)
    timeperiod              = models.TimeField(auto_now_add =True)
    trad_type               = models.CharField(max_length=250)
    starting_asset_price    = models.FloatField(default = 0.0)
    ending_asset_price      = models.FloatField(default = 0.0)
    trad_status             = models.SmallIntegerField(choices = TRAD_STATUS)

    def __str__(self):
        return self.user_id.username

NEWS_STATUS = [
                (1, 'Active'),
                (0, 'Inactive'),    
            ]

class News(models.Model):
    '''
        Model class for managing the News
    '''

    name                    = models.CharField(max_length=250)
    date                    = models.DateTimeField(auto_now_add =True)
    time                    = models.TimeField(auto_now_add= True)
    new_type                = models.CharField(max_length = 250)
    category                = models.CharField(max_length = 250)
    author                  = models.CharField(max_length =250)
    video_file              = models.FileField(upload_to ='videos/',null=True , blank=True)
    status                  = models.SmallIntegerField(choices = NEWS_STATUS)

    def __str__(self):
        return self.name
