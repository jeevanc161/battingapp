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

app_name = 'dashboard'

urlpatterns = [
    path('login/' , LoginView.as_view() , name='login'),
    path('logout/' , LogoutView.as_view() , name='logout'),
    path('' , views.AdminIndexPageView.as_view() , name = 'admin_index'),

    # List of URL Path for the User
    path('list_user/', views.UserListPageView.as_view() , name = 'user_list'),
    path('<int:pk>/', views.UserDetailPageView.as_view() , name = 'user_detail'),
    path('delete/<int:id>' , views.UserDeletePageView.as_view() , name= 'user_delete'),
    path('update/<int:pk>', views.UserUpdatePageView.as_view() , name = 'user_update' ),
    path('create/' , views.UserCreatePageView.as_view() , name = 'user_create'),
    path('user_document/<int:pk>' , views.UserDocumentPageView.as_view() , name = 'user_document'),
    path('user_deposit_history/<int:pk>' , views.UserDepositHistoryPageView.as_view() , name = 'user_deposit_history'),
    path('user_withdraw_history/<int:pk>' , views.UserWithdrawHistoryPageView.as_view() , name = 'user_withdraw_history'),
    path('user_account/<int:pk>' , views.UserAccountDetailPageView.as_view() , name = 'user_account_detail'),

    path('csv-export/' , views.csv_user_write , name = 'csv_export'),
    path('pdf-export/' , views.pdf_user_view , name = 'pdf_export'),

    # List of URL Path for the Asserts
    path('assets/' , views.AssertListPageView.as_view() , name = 'assets_list'),
    path('assets/create' , views.AssertCreatePageView.as_view() , name = 'assets_create'),
    path('assets/delete/<int:id>' , views.AssetsDeletePageView.as_view() , name = 'assets_delete'),
    path('assets/update/<int:pk>' , views.AssetsUpdatePageView.as_view() , name = 'assets_update'),
    path('assets/detail/<int:pk>' , views.AssetsDetailPageView.as_view() , name = 'assets_detail'),
    
    # List of URL Path for the Deposit History
    path('deposit_history/' , views.DepositHistoryListPageView.as_view() , name = 'deposit_history_list'),
    path('deposit_history/create' , views.DepositHistoryCreatePageView.as_view() , name = 'deposit_history_create'),
    path('deposit_history/delete/<int:id>' , views.DepositHistoryDeletePageView.as_view() , name = 'deposit_history_delete'),
    path('deposit_history/update/<int:pk>' , views.DepositHistoryUpdatePageView.as_view() , name = 'deposit_history_update'),
    path('deposit_history/detail/<int:pk>' , views.DepositHistoryDetailPageView.as_view() , name = 'deposit_history_detail'),

    # List of URL Path for News
    path('news/' , views.NewsListPageView.as_view() , name = 'news_list'),
    path('news/create' , views.NewsCreatePageView.as_view() , name = 'news_create'),
    path('news/delete/<int:id>' , views.NewsDeletePageView.as_view() , name = 'news_delete'),
    path('news/update/<int:pk>' , views.NewsUpdatePageView.as_view() , name = 'news_update'),
    path('news/detail/<int:pk>' , views.NewsDetailPageView.as_view() , name = 'news_detail'),

    # List of URL Path for Deposit Offers
    path('deposit_offer/' , views.DepositOfferListPageView.as_view() , name = 'deposit_offer_list'),
    path('deposit_offer/create' , views.DepositOfferCreatePageView.as_view() , name = 'deposit_offer_create'),
    path('deposit_offer/delete/<int:id>' , views.DepositOfferDeletePageView.as_view() , name = 'deposit_offer_delete'),
    path('deposit_offer/update/<int:pk>' , views.DepositOfferUpdatePageView.as_view() , name = 'deposit_offer_update'),
    path('deposit_offer/detail/<int:pk>' , views.DepositOfferDetailPageView.as_view() , name = 'deposit_offer_detail'),

    # List of URL Path for Deposit Offers
    path('withdraw_history/' , views.WithdrawHistoryListPageView.as_view() , name = 'withdraw_history_list'),
    path('withdraw_history/create' , views.WithdrawHistoryCreatePageView.as_view() , name = 'withdraw_history_create'),
    path('withdraw_history/delete/<int:id>' , views.WithdrawHistoryDeletePageView.as_view() , name = 'withdraw_history_delete'),
    path('withdraw_history/update/<int:pk>' , views.WithdrawHistoryUpdatePageView.as_view() , name = 'withdraw_history_update'),
    path('withdraw_history/detail/<int:pk>' , views.WithdrawHistoryDetailPageView.as_view() , name = 'withdraw_history_detail'),

    # List of URL Path for Withdraw Request
    path('withdraw_request/' , views.WithdrawRequestListPageView.as_view() , name = 'withdraw_request_list'),
    path('withdraw_request/create' , views.WithdrawRequestCreatePageView.as_view() , name = 'withdraw_request_create'),
    path('withdraw_request/delete/<int:id>' , views.WithdrawRequestDeletePageView.as_view() , name = 'withdraw_request_delete'),
    path('withdraw_request/update/<int:pk>' , views.WithdrawRequestUpdatePageView.as_view() , name = 'withdraw_request_update'),
    path('withdraw_request/detail/<int:pk>' , views.WithdrawRequestDetailPageView.as_view() , name = 'withdraw_request_detail'),

    # List of URL Path for Trad History
    path('trad_history/' , views.TradHistoryListPageView.as_view() , name = 'trad_history_list'),
    path('trad_history/create' , views.TradHistoryCreatePageView.as_view() , name = 'trad_history_create'),
    path('trad_history/delete/<int:id>' , views.TradHistoryDeletePageView.as_view() , name = 'trad_history_delete'),
    path('trad_history/update/<int:pk>' , views.TradHistoryUpdatePageView.as_view() , name = 'trad_history_update'),
    path('trad_history/detail/<int:pk>' , views.TradHistoryDetailPageView.as_view() , name = 'trad_history_detail'),

]
 