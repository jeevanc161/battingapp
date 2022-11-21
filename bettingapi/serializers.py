from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from dashboard.models import User
from bettingapp.models import (
                            	MarketGame,
                                GamePrice,
                                UserBetting,
                                DepositHistory,
                                WithdrawRequest,
                                MarketGameBiddingType,
                            )

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (  'pk', 'username', 'email', 'password', 'first_name', 'last_name',
        			'phone_number' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'], 
            email = validated_data['email'], 
            password = make_password(validated_data['password']),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'] ,
            phone_number = validated_data['phone_number'], 
            is_betting_user = True
        	)

        return user 


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id' , 'account_holder_name' , 'bank_account_number' ,
                    'bank_name' , 'ifsc_code']


# Market Game's API
class MarketGameSerializer(serializers.ModelSerializer):

	class Meta:
		model = MarketGame
		fields = [ 'id' , 'name','market_type' ,'game_type' , 
                    'game_type_open',  'game_type_close','open_time' , 
					'close_time' , 'open_result_time' , 'close_result_time' ,
					'open_single_result' ,'open_triple_result' , 
					'close_single_result' ,'close_triple_result' ,
					'close_jodi_result' , 'status'
				]

 # Star Line Market Game's API
class StarLineGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketGame
        fields = [ 'id' , 'name','market_type' ,'game_type' , 
                     'game_type_close', 'close_time' , 'open_result_time',
                    'close_jodi_result' , 'status'
                ]


class GamePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePrice
        fields = [ 'id' , 'name','market_type' , 'bet_amount' , 'win_amount' ]



class UserBiddingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBetting
        fields = '__all__'


class DepositHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositHistory
        fields = '__all__'



class WithdrawRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = WithdrawRequest
        fields = '__all__'

class MarketGameBiddingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketGameBiddingType
        fields = [ 'id' , 'name' , 'market_type']