from django.urls import path
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from . import views



app_name = 'api'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileAPIView.as_view(), name='user_profile'),
    
    path('assets/', views.AssertListAPIView.as_view() , name = 'assets'),
    path('assets/<int:pk>/', views.AssertDtailAPIView.as_view() , name = 'asset'),
    
    path('deposit_history/', views.DepositHistoryAPIView.as_view()),
    path('deposit_history/<int:pk>/', views.DepositHistoryDetailAPIView.as_view()),
    
    path('deposit_offer/', views.DepositOfferAPIView.as_view()),
    path('deposit_offer/<int:pk>/', views.DepositOfferDetailAPIView.as_view()),
    
    path('withdraw_history/', views.WithdrawHistoryAPIView.as_view()),
    path('withdraw_history/<int:pk>/', views.WithdrawHistoryDetailAPIView.as_view()),

    path('withdraw_request/', views.WithdrawRequestAPIView.as_view()),
    path('withdraw_request/<int:pk>/', views.WithdrawRequestDetailAPIView.as_view()),

    path('trad_history/', views.TradHistoryAPIView.as_view()),
    path('trad_history/<int:pk>/', views.TradHistoryDtailAPIView.as_view()),

    path('news/', views.NewsAPIView.as_view()),
    path('news/<int:pk>/', views.NewsDtailAPIView.as_view()),
] 