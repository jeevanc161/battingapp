from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render , redirect , reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic 
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from knox.models import AuthToken
from django.db.models import Sum , Count
from dashboard.utils import render_to_pdf # FOR PDF EXPORT
from django.template.loader import get_template #FOR PDF EXPORT
from dashboard.models import User 
from bettingapp.form import ( BettingUserForm ,
								MarketForm , 
								StarLineMarketForm , 
								GamePriceForm ,
								MainMarketResultForm,
								)
from bettingapp.models import( DepositHistory ,
								MarketGame, 
								GamePrice , 
								UserBetting , 
								WithdrawHistory,
								WithdrawRequest,
								UserWinner,
								)


class BettingDashboardPageView(LoginRequiredMixin, generic.TemplateView):
	"""
		Get Admin Dashboard Page View and display Data
	"""
	template_name = 'bettingapp/dashboard2.html'

	def get_context_data(self, **kwargs):
		context =  super(BettingDashboardPageView , self).get_context_data(**kwargs)
		date = timezone.now().date()

		main_bidding_users = UserBetting.objects.filter(created_date__gte = date,
								market_type = 'main').values('market_id__name'
								).annotate(total_users = Count('user_id')).annotate(total_amount= Sum('bidding_points'))
		star_line_bidding_users = UserBetting.objects.filter(created_date__gte = date, 
								market_type = 'starline').values('market_id__name').annotate(total_users = Count('user_id')
								).annotate(total_amount= Sum('bidding_points'))

		month_withdraw = WithdrawHistory.objects.all()
		withdraw_total_amount = month_withdraw.aggregate(Sum('amount'))
		withdraw_total_users = month_withdraw.aggregate(Count('user_id'))

		month_deposit = DepositHistory.objects.all()
		deposit_total_amount = month_deposit.aggregate(Sum('amount'))
		deposit_total_users = month_deposit.aggregate(Count('user_id'))

		context.update({
			'main_bidding_users' : main_bidding_users,
			'star_line_bidding_users' : star_line_bidding_users,
			'withdraw_total_amount' : withdraw_total_amount,
			'withdraw_total_users' : withdraw_total_users,
			'deposit_total_amount' : deposit_total_amount,
			'deposit_total_users' : deposit_total_users


		})
		return context


class BettingUserListPageView(LoginRequiredMixin, generic.ListView):
	"""
		Display list of all Betting application users
	"""
	template_name = 'bettingapp/users_list.html'
	context_object_name = 'users'

	def get_queryset(self):
		queryset = User.objects.filter(is_betting_user  = True).order_by('-account_created_date')
		return queryset


class BettingUserDetailPageView(LoginRequiredMixin , generic.DetailView):
	"""
		Display the details view of the User data 
	"""
	template_name = 'bettingapp/user_detail.html'
	context_object_name = 'user'

	def get_queryset(self):
		queryset = User.objects.all()
		return queryset


class BettingUserDeletePageView(LoginRequiredMixin, generic.RedirectView): 
	"""
		Delete a Betting user and redirect to the Betting User List View
	"""
	url = '/admin/bettingapp/users/'  

	def get_redirect_url(self , *args , **kwargs):
		del_id = kwargs['id']
		AuthToken.objects.filter(user_id = del_id).delete()
		User.objects.get(id = del_id).delete()
		return super().get_redirect_url(*args , **kwargs)


class BettingUserDepositHistoryPageView(LoginRequiredMixin , generic.ListView):
	'''
		all deposit history record according to the user
	'''
	template_name = 'bettingapp/user_deposit_history_detail.html'
	context_object_name = 'user_deposit_history'

	def get_queryset(self):
		pk = self.kwargs['pk']
		queryset = DepositHistory.objects.filter(user_id = pk).order_by('-transaction_date')
		return queryset

	def get_context_data(self, **kwargs):
		context =  super(BettingUserDepositHistoryPageView , self).get_context_data(**kwargs)
		context.update({
			'pk' : self.kwargs['pk'] , 
		})
		return context


class BettingUserBettingListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the User Betting data in list view 
	"""
	template_name = 'bettingapp/user_bidding_history_detail.html'
	context_object_name = 'user_bettings'

	def get_queryset(self):
		pk = self.kwargs['pk']
		queryset = UserBetting.objects.filter(user_id = pk).order_by('-bidding_date')
		return queryset

	def get_context_data(self, **kwargs):
		context =  super(BettingUserBettingListPageView , self).get_context_data(**kwargs)
		context.update({
			'pk' : self.kwargs['pk'] , 
		})
		return context


class BettingUserUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
	"""
		Update the user data and and display a success message to the admin side
	"""
	template_name = 'bettingapp/user_update.html'
	form_class = BettingUserForm
	success_message = 'Profile successfully Updated!!!!'

	def get_queryset(self):
		return User.objects.all()

	def get_success_url(self):
		# messages.success(request,"Profile Updated!")
		return reverse('bettingapp:betting_user_update' , kwargs = {'pk': self.get_object().id})



class NormalMarketListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Assert List and render to the Normal Market List view in admin site
	"""
	template_name = 'bettingapp/normal_market_list.html'
	context_object_name = 'normal_markets'

	def get_queryset(self):
		queryset = MarketGame.objects.filter(market_type = 0).order_by('name')
		return queryset
		

class NormalMarketCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
	"""
		Create a Assert with this class based view
	"""

	template_name = 'bettingapp/normal_market_create.html'
	form_class = MarketForm
	success_message = "New Market Created successfully!!!!"

	def get_success_url(self):
		return reverse('bettingapp:normal_market_list')

	def form_valid(self, form):
		form.save()
		return super(NormalMarketCreatePageView , self).form_valid(form)



class NormalMarketUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
	"""
		Update the Assets data and and display a success message to the admin side
	"""
	template_name = 'bettingapp/normal_market_update.html'
	form_class = MarketForm
	success_message = 'Normal Market successfully Updated!!!!'

	def get_queryset(self):
		return MarketGame.objects.all()

	def get_success_url(self):
		return reverse('bettingapp:normal_market_update' , kwargs = {'pk': self.get_object().id})


class NormalMarketDetailPageView(LoginRequiredMixin , generic.DetailView):
	'''
		Detail view for the assets data
	'''
	template_name = 'bettingapp/normal_market_detail.html'
	context_object_name = 'normal_market'

	def get_queryset(self):
		queryset = MarketGame.objects.all()
		return queryset


class StarLineMarketListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Assert List and render to the Normal Market List view in admin site
	"""
	template_name = 'bettingapp/star_line_market_list.html'
	context_object_name = 'normal_markets'

	def get_queryset(self):
		queryset = MarketGame.objects.filter(market_type = 1).order_by('close_time')
		return queryset
		

class StarLineMarketCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
	"""
		Create a Assert with this class based view
	"""

	template_name = 'bettingapp/star_line_market_create.html'
	form_class = StarLineMarketForm
	success_message = "New Market Created successfully!!!!"

	def get_success_url(self):
		return reverse('bettingapp:star_line_market_list')

	def form_valid(self, form):
		form.save()
		return super(StarLineMarketCreatePageView , self).form_valid(form)


class StarLineMarketUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
	"""
		Update the Assets data and and display a success message to the admin side
	"""
	template_name = 'bettingapp/star_line_market_update.html'
	form_class = StarLineMarketForm
	success_message = 'Market details successfully Updated!!!!'

	def get_queryset(self):
		return MarketGame.objects.all()

	def get_success_url(self):
		return reverse('bettingapp:star_line_market_update' , kwargs = {'pk': self.get_object().id})



class GamePriceListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Assert List and render to the Normal Market List view in admin site
	"""
	template_name = 'bettingapp/game_price_list.html'
	context_object_name = 'game_prices'

	def get_queryset(self):
		queryset = GamePrice.objects.all().order_by('market_type')
		return queryset
	

class GamePriceUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
	"""
		Update the Assets data and and display a success message to the admin side
	"""
	template_name = 'bettingapp/game_price_market_update.html'
	form_class = GamePriceForm
	success_message = 'Game Price successfully Updated!!!!'

	def get_queryset(self):
		return GamePrice.objects.all()

	def get_success_url(self):
		return reverse('bettingapp:game_price_update' , kwargs = {'pk': self.get_object().id})
 

class UserBettingListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the User Betting data in list view 
	"""
	template_name = 'bettingapp/user_betting_list.html'
	context_object_name = 'user_bettings'

	def get_queryset(self):
		queryset = UserBetting.objects.all()
		return queryset


class UserBettingDetailPageView(LoginRequiredMixin , generic.DetailView):
	'''
		Detail view for the assets data
	'''
	template_name = 'bettingapp/user_betting_detail.html'
	context_object_name = 'user_betting'

	def get_queryset(self):
		queryset = UserBetting.objects.all()
		return queryset


class DepositHistoryListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Deposit History List and render to the assert List view in admin site
	"""
	template_name = 'bettingapp/deposit_history_list.html'

	context_object_name = 'deposit_historys'

	def get_queryset(self):
		queryset = DepositHistory.objects.all().order_by('-transaction_date')
		return queryset


class DepositHistoryDeletePageView(LoginRequiredMixin,  generic.RedirectView): 
	"""
		Delete a Deposit History and redirect to the Asset List View
	"""
	url = '/admin/bettingapp/deposit-history/'  
	# success_message = 'Deposit History successfully Deleted!!!!'

	def get_redirect_url(self , *args , **kwargs):
		del_id = kwargs['id']
		DepositHistory.objects.get(id = del_id).delete()
		return super().get_redirect_url(*args , **kwargs)


class DepositHistoryDetailPageView(LoginRequiredMixin , generic.DetailView):
	'''
		Detail view for the Deposit History  data
	'''
	template_name = 'bettingapp/deposit_history_detail.html'
	context_object_name = 'deposit_history'

	def get_queryset(self):
		queryset = DepositHistory.objects.all()
		return queryset


class WithdrawHistoryListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Withdraw Histroy List and render to the Widhdraw History List view in admin site
	"""
	template_name = 'bettingapp/withdrow_history_list.html'
	# paginate_by = 10
	context_object_name = 'withdraw_historys'

	def get_queryset(self):
		queryset = WithdrawHistory.objects.filter(status = 1).order_by('-transaction_date')
		return queryset


class WithdrawHistoryDetailPageView(LoginRequiredMixin , generic.DetailView):
	'''
		Detail view for the Withdraw History data
	'''
	template_name = 'bettingapp/withdraw_history_detail.html'
	context_object_name = 'withdraw_history'

	def get_queryset(self):
		queryset = WithdrawHistory.objects.all()
		return queryset


class WithdrawHistoryDeletePageView(LoginRequiredMixin, generic.RedirectView): 
	"""
		Delete a Deposit Offer and redirect to the Asset List View
	"""
	url = '/admin/bettingapp/withdraw-history/'  

	def get_redirect_url(self , *args , **kwargs):
		del_id = kwargs['id']
		WithdrawHistory.objects.get(id = del_id).delete()
		return super().get_redirect_url(*args , **kwargs)   


class WithdrawRequestListPageView(LoginRequiredMixin , generic.ListView):
	"""
		Get all the Withdraw Histroy List and render to the Widhdraw History List view in admin site
	"""
	template_name = 'bettingapp/withdrow_request_list.html'
	# paginate_by = 10
	context_object_name = 'withdraw_requests'

	def get_queryset(self):
		queryset = WithdrawRequest.objects.filter(status__in = [0 , 2] )
		return queryset


class WithdrawRequestDeletePageView(LoginRequiredMixin, generic.RedirectView): 
	"""
		Delete a Deposit Offer and redirect to the Asset List View
	"""
	url = '/admin/bettingapp/withdraw-request/'  

	def get_redirect_url(self , *args , **kwargs):
		del_id = kwargs['id']
		WithdrawRequest.objects.get(id = del_id).delete()
		return super().get_redirect_url(*args , **kwargs)   


class WithdrawRequestDetailPageView(LoginRequiredMixin , generic.DetailView):
	'''
		Detail view for the Withdraw History data
	'''
	template_name = 'bettingapp/withdraw_request_detail.html'
	context_object_name = 'withdraw_request'

	def get_queryset(self):
		queryset = WithdrawRequest.objects.all()
		return queryset


class MainMarketDeclareResultPageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
	"""
		THis view handle the request and pag redirect to the result declation of the main Market games
	"""
	template_name = 'bettingapp/normal_market_declare_result.html'
	form_class = MainMarketResultForm
	success_message = 'Result Updated Sucsessfully!!!!'
	context_object_name = 'main_market'

	def get_queryset(self):
		return MarketGame.objects.all()

	def get_success_url(self):
		return reverse('bettingapp:main_market_declare_result' , kwargs = {'pk': self.get_object().id})


class UserWinnerListPageView(LoginRequiredMixin , generic.ListView):
	"""
		view class for the Winner users to get and render on the admin site
	"""
	template_name = 'bettingapp/user_winner_list.html'
	context_object_name = 'user_winners'

	def get_queryset(self):
		queryset =  UserWinner.objects.all()
		return queryset