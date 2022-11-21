from django.urls import path
from knox import views as knox_views
from . import views


 
app_name = 'bettingapi'

urlpatterns = [

    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('account-detail/<int:pk>', views.AccountDetailsUpdateAPIView.as_view() ),

    # market game url paths
    path('market_game/', views.MarketGameListAPIView.as_view()),
    path('star_line_game/', views.StarLineMarketGameListAPIView.as_view()),
    path('main-game-price/' , views.MainGamePriceListAPIView.as_view()),
    path('starline-game-price/' , views.StarLineGamePriceListAPIView.as_view()),
    path('main-game-bidding-type/' , views.MainGamesBiddingTypeAPIView.as_view()),
    path('starline-game-bidding-type/' , views.StarLineGameBiddingTypeAPIVIew.as_view()),

    # bidding game url paths
    path('user-bidding/<int:pk>', views.UserBiddingListAPIView.as_view()),
    path('single-digit-bidding/<int:pk>', views.SingleDigitUserBettingListAPIView.as_view()),
    path('main-jodi-digit-bidding/<int:pk>', views.MainJodiDigitUserBettingListAPIView.as_view()),
    path('single-patti-bidding/<int:pk>', views.SinglePattiUserBettingListAPIView.as_view()),
    path('double-patti-bidding/<int:pk>', views.DoublePattiUserBettingListAPIView.as_view()),
    path('triple-patti-bidding/<int:pk>', views.TriplePattiUserBettingListAPIView.as_view()),
    

    # URL path for the Top winners
    path('deposit-history/' , views.DepositHistoryCreateListAPIView.as_view()),
    path('withdraw-request/' , views.WithdrawRequestCreateListAPIView.as_view()), 
    path('top-main-games-winner/' , views.TopWinnersMainListAPIView.as_view()),
    path('top-starline-games-winner/' , views.TopWinnersStarLineListAPIView.as_view()),

      
   
] 