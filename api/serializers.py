from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django_countries.serializers import CountryFieldMixin
from dashboard.models import (User , 
                            Assets , 
                            DepositHistory, 
                            DepositOffers , 
                            WithdrawHistory ,
                            WithdrawRequest,
                            TradHistory,
                            News,)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(CountryFieldMixin , serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (  'pk', 'username', 'email', 'password', 'first_name', 'last_name','middle_name', 
                    'phone_number' , 'country','city' , 'dob' , 'status' ,'login_status' ,'profile_picture' , 
                    'aadhar_card','pen_card' , 'bank_passbook' , 'bank_account_number', 'bank_name' , 'ifsc_code', 
                    'wallet_amount' , 'total_bonus_amount' , 'account_opening_bonus')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'], 
            email = validated_data['email'], 
            password = make_password(validated_data['password']),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'] ,
            phone_number = validated_data['phone_number'], 
        	)

        return user 


class AssetsSerializer(serializers.ModelSerializer):
    """
        Serializer Class for the Assets
    """    
    class Meta:
        model = Assets
        fields = ('id' ,'name' , 'icon' , 'current_market_price' , 'yesterday_price' , 
                    'returns' , 'increament_decreament' , 'active')



class DepositHistorySerializer(serializers.ModelSerializer):
    """
        Serializer Class for the DepositHistory
    """       
    class Meta:
        model = DepositHistory
        fields = ('id' ,'user_id' , 'transaction_date' , 'transaction_time' , 'amount' , 
                    'bonus_amount' , 'payment_id' , 'payment_mode' , 'payment_source',
                    'status')



class DepositOfferSerializer(serializers.ModelSerializer):
    """
        Serializer Class for the Deposit Offer Serializer 
    """

    class Meta :
        model = DepositOffers
        fields = ( 'id' , 'name' , 'deposit_amount' , 'bonus_amount' ,
                    'date' , 'status' )


class WithdrawHistorySerializer(serializers.ModelSerializer):
    """
        Serializer Class for the Withdraw history  Serializer 
    """

    class Meta :
        model = WithdrawHistory
        fields = ( 'id', 'user_id' , 'transaction_date' , 'transaction_time' , 'amount' ,
                    'payment_id' , 'payment_mode' , 'payment_source' , 'status' , 'remarks' )


class WithdrawRequestSerializer(serializers.ModelSerializer):
    """
        Serializer Class for the Withdraw Request
    """

    class Meta:
        model = WithdrawRequest
        fields = ('id' ,'user_id', 'request_amount' ,  'date_time' , 'status')


class TradHistorySerializer(serializers.ModelSerializer):
    """
        Serializer Class for the rad History
    """

    class Meta :
        model = TradHistory
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    """
        Serializer Class for the News
    """

    class Meta:
        model = News
        fields = "__all__"