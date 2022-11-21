from django import forms
from django.forms import fields
from .models import (User , Assets , DepositHistory , News , DepositOffers
					  , WithdrawHistory , WithdrawRequest , TradHistory )

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = [ 'username', 'first_name' , 'middle_name' , 'last_name',
				   'email', 'phone_number' ,'dob' , 'country' , 'city' ,'profile_picture',
				   'aadhar_card' , 'pen_card' , 'bank_passbook' , 'bank_account_number' , 'bank_name',
				   'ifsc_code' , 'wallet_amount' , 'total_bonus_amount' , 'account_opening_bonus']

		widgets = {
            'country' : forms.Select(attrs={'class' : 'form-control'}),  
        }

        
class UserCreateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = '__all__'


	def __init__(self, *args, **kwargs):
		from django.forms.widgets import HiddenInput
        # hide_condition = kwargs.pop('hide_condition',None)
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields['last_login'].widget = HiddenInput()
		self.fields['groups'].widget = HiddenInput()
		self.fields['user_permissions'].widget = HiddenInput()


class AssetsFrom(forms.ModelForm):
	
	class Meta:
		model = Assets
		fields = ['name' , 'icon' , 'current_market_price' , 'yesterday_price' , 
					'returns' , 'increament_decreament' ,'active' ]


class DepositHistoryForm(forms.ModelForm):
	
	class Meta:
		model = DepositHistory
		fields = '__all__'


class NewsForm(forms.ModelForm):

	class Meta:
		model = News
		fields = '__all__'

		widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),  
        }


class DepositOfferForm(forms.ModelForm):

	class Meta:
		model = DepositOffers
		fields = '__all__'

		widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),  
        }


class WithdrawHistoryForm(forms.ModelForm):

	class Meta:
		model = WithdrawHistory
		fields = "__all__"

		widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),  
            'user_id' : forms.Select(attrs={'class' : 'form-control'}), 
        }


class WithdrawRequestForm(forms.ModelForm):

	class Meta:
		model = WithdrawRequest
		fields = "__all__"

		widgets = {
            'status' : forms.Select(attrs={'class' : 'form-control'}),  
            'user_id' : forms.Select(attrs={'class' : 'form-control'}), 
        }


class TradHistoryForm(forms.ModelForm):

	class Meta:
		model = TradHistory
		fields = "__all__"