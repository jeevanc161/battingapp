from django.urls import path 
from django.contrib.auth.views import ( 
    LoginView, 
    LogoutView, 
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views

app_name = 'bettingapp'

urlpatterns = [

    path('' , views.BettingDashboardPageView.as_view() , name = 'betting_dashboard'),

    # List of URL for the Users
    path('users/' , views.BettingUserListPageView.as_view() , name = 'users_list'),
    path('detail/<int:pk>' , views.BettingUserDetailPageView.as_view() , name= 'user_detail') ,
    path('delete/<int:id>/' , views.BettingUserDeletePageView.as_view() , name = 'users_delete'),
    path('update/<int:pk>/' , views.BettingUserUpdatePageView.as_view() , name = 'betting_user_update'),
    path('user_deposit_history/<int:pk>/' , views.BettingUserDepositHistoryPageView.as_view() , name = 'user_deposit_history'),
    path('user_betting_history/<int:pk>/' , views.BettingUserBettingListPageView.as_view() , name = 'user_betting_history'),

    # List of URL Path for the Market 
    path('main_market/' , views.NormalMarketListPageView.as_view() , name = 'normal_market_list'),
    path('main_market/create' , views.NormalMarketCreatePageView.as_view() , name = 'normal_market_create'),
    path('main_market/update/<int:pk>' , views.NormalMarketUpdatePageView.as_view() , name = 'normal_market_update'),
    path('main_market/detail/<int:pk>' , views.NormalMarketDetailPageView.as_view() , name = 'normal_market_detail'),
    path('main_market/main_market_result/<int:pk>' , views.MainMarketDeclareResultPageView.as_view() , name = 'main_market_declare_result'),
    # List of URL Path for the Star Line Market 
    path('star-line-market/' , views.StarLineMarketListPageView.as_view() , name = 'star_line_market_list'),
    path('star-line-market/create' , views.StarLineMarketCreatePageView.as_view() , name = 'star_line_market_create'),
    path('star-line-market/update/<int:pk>' , views.StarLineMarketUpdatePageView.as_view() , name = 'star_line_market_update'),
    # path('main_market/detail/<int:pk>' , views.NormalMarketDetailPageView.as_view() , name = 'normal_market_detail'),
    
    # List of URL Path for the Game Price 
    path('game-price/' , views.GamePriceListPageView.as_view() , name = 'game_price_list'),
    path('game-price/update/<int:pk>' , views.GamePriceUpdatePageView.as_view() , name = 'game_price_update'),
    
    # List of URL Path for the  User Betting 
    path('user-betting/' , views.UserBettingListPageView.as_view() , name = 'user_betting_list'),
    path('user-betting/detail/<int:pk>' , views.UserBettingDetailPageView.as_view() , name = 'user_betting_detail'),
    
    # List of url path for the Winners
    path('user-winners/' , views.UserWinnerListPageView.as_view() , name = 'user_winner_list'),

    # List of url path for deposit history 
    path('deposit-history/' , views.DepositHistoryListPageView.as_view() , name = 'user_deposit_history'),
    path('deposit-history/delete/<int:id>/' , views.DepositHistoryDeletePageView.as_view() , name = 'deposit_history_delete'),
    path('deposit-history/detail/<int:pk>' , views.DepositHistoryDetailPageView.as_view() , name = 'deposit_history_detail'),

    # List of URL Path for Withdraow History
    path('withdraw-history/' , views.WithdrawHistoryListPageView.as_view() , name = 'withdraw_history_list'),
    path('withdraw-history/delete/<int:id>' , views.WithdrawHistoryDeletePageView.as_view() , name = 'withdraw_history_delete'),
    path('withdraw-history/detail/<int:pk>' , views.WithdrawHistoryDetailPageView.as_view() , name = 'withdraw_history_detail'),

    # List of url path for withdraw request
    path('withdraw-request/' , views.WithdrawRequestListPageView.as_view() , name = 'withdraw_request_list'),
    path('withdraw-request/delete/<int:id>' , views.WithdrawRequestDeletePageView.as_view() , name = 'withdraw_request_delete'),
    path('withdraw-request/detail/<int:pk>' , views.WithdrawRequestDetailPageView.as_view() , name = 'withdraw_request_detail'),


]   
    