from datetime import datetime
from django import forms
from django.forms import fields
from dashboard.models import (User)
from bettingapp.models import MarketGame , GamePrice , UserBetting ,UserWinner ,MarketGameBiddingType

class BettingUserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = [ 'username', 'first_name' ,  'last_name','email', 
				'phone_number' , 'bank_account_number' , 'bank_name',
				 'account_holder_name',  'ifsc_code'  ]

class MarketForm(forms.ModelForm):

	class Meta:
		model = MarketGame
		fields = [ 'name' , 'market_type' , 'open_time' , 'close_time',
					'open_result_time' , 'close_result_time' , 'status']

		widgets = {
			'market_type' : forms.Select(attrs={'class' : 'form-control'}),  
			'status' : forms.Select(attrs={'class' : 'form-control'}), 
		}

class MainMarketResultForm(forms.ModelForm):
	market_id = forms.IntegerField()
	class Meta:
		model = MarketGame
		fields = [  'open_triple_result' , 'open_single_result' , 'close_single_result' , 
					'close_triple_result' , 'close_jodi_result' ]


	def winning_amount(self , price_id, amount):

		if price_id == 1:
			amount *= 9
		elif price_id == 2:
			amount *= 95
		elif price_id == 3:
			amount *= 140
		elif price_id == 4:
			amount *= 280
		elif price_id == 5:
			amount *= 600
		elif price_id == 6:
			amount *= 1000
		else:
			amount

		return amount

	def save(self , *args , **kwargs):
		date = datetime.now().date()
		betting_users = UserBetting.objects.filter(bidding_date__gte = date,
									market_id = self.cleaned_data['market_id'] ,
									bidding_digit__in = [self.cleaned_data['open_triple_result'], 
														self.cleaned_data['open_single_result'],
														self.cleaned_data['close_single_result'],
														self.cleaned_data['close_triple_result'],
														self.cleaned_data['close_jodi_result'],])
		for betting_user in betting_users:
			if UserWinner.objects.filter(user_bidding_id = betting_user.id).exists():
				pass
			else:
				# import pdb ; pdb.set_trace()
				UserWinner.objects.create(
					user_bidding_id = UserBetting.objects.get(id = betting_user.id),
					user_id = User.objects.get(id = betting_user.user_id.id),
					market_id = MarketGame.objects.get(id =betting_user.market_id.id) ,
					market_game_bidding_type_id = MarketGameBiddingType.objects.get(id = betting_user.market_game_bidding_type_id.id),
					market_type = betting_user.market_type,
					game_category = betting_user.game_category,
					bidding_digit = betting_user.bidding_digit,
					win_bidding_digit = self.winning_amount(betting_user.market_game_bidding_type_id.id , betting_user.bidding_points) ,
					bidding_points = betting_user.bidding_points ,
					bidding_date = betting_user.bidding_date,
					bidding_time = betting_user.bidding_time 
				)
				
				user = User.objects.get(id = betting_user.user_id.id)
				user.wallet_amount = user.wallet_amount + self.winning_amount(betting_user.market_game_bidding_type_id.id , betting_user.bidding_points)
				user.save()

		super(MainMarketResultForm, self).save(*args, **kwargs)


class StarLineMarketForm(forms.ModelForm):

	class Meta:
		model = MarketGame
		fields = [ 'name' , 'market_type' , 'open_time' , 'close_time',
					'open_result_time' , 'close_result_time' , 'status']

		widgets = {
			'market_type' : forms.Select(attrs={'class' : 'form-control'}),  
			'status' : forms.Select(attrs={'class' : 'form-control'}), 
		}


class GamePriceForm(forms.ModelForm):

	class Meta:
		model = GamePrice
		fields = [ 'name' , 'market_type' , 'bet_amount' , 'win_amount']
		widgets = {
			'market_type' : forms.Select(attrs={'class' : 'form-control'}),  
			}

