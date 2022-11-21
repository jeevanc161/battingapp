from datetime import datetime
from django.http import Http404
from rest_framework import permissions ,generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from django.db.models.aggregates import Max
from dashboard.models import User
from bettingapp.models import( MarketGame , GamePrice , UserBetting , MarketGameBiddingType) 
from .serializers import (
    MarketGameSerializer,
    RegisterSerializer,
    UserSerializer,
    AccountSerializer,
    StarLineGameSerializer,
    GamePriceSerializer,
    UserBiddingSerializer,
    DepositHistorySerializer, 
    WithdrawRequestSerializer,
    MarketGameBiddingTypeSerializer,
)
 
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
            'wallet_amount' : request.user.wallet_amount ,
            'phone_number' : request.user.phone_number
        }
        
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data 

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_betting_user:
            login(request, user)
        else :
            message = {"meesage" : "You are not Valid User"}
            return Response(message , status=status.HTTP_204_NO_CONTENT)
        return super(LoginAPI, self).post(request, format=None)
 

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        name  = request.data['name'].split(" ")
        first_name = name[0]
        if len(name)>1:
            last_name = ' '.join(name[1:])
        else:
            last_name = ''
        user.update({'first_name' : first_name ,
                    'last_name' : last_name })        
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class AccountDetailsUpdateAPIView(APIView):
    """
    Account details of the user and update and display
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk , format=None):
        user = self.get_object(pk)
        serializer = AccountSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk , format=None):
        user = self.get_object(pk)
        serializer = AccountSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class MarketGameListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        games = MarketGame.objects.filter(market_type = 0)
        serializer = MarketGameSerializer(games, many=True)
        return Response(serializer.data)


class StarLineMarketGameListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        games = MarketGame.objects.filter(market_type = 1)
        serializer = StarLineGameSerializer(games, many=True)
        return Response(serializer.data)


class MainGamePriceListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , format =None):
        game_rate = GamePrice.objects.filter(market_type = 0)
        serializer = GamePriceSerializer(game_rate , many = True)
        return Response(serializer.data)



class StarLineGamePriceListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , format =None):
        game_rate = GamePrice.objects.filter(market_type = 1)
        serializer = GamePriceSerializer(game_rate , many = True)
        return Response(serializer.data)


class MainGamesBiddingTypeAPIView(APIView):
    """
        this api work for the getting user betting type like - single jodi double etc.
    """
    def get(self , request , format =None):
        bidding_type = MarketGameBiddingType.objects.filter(market_type = 0)
        serializer = MarketGameBiddingTypeSerializer(bidding_type , many = True)
        return Response(serializer.data)

class StarLineGameBiddingTypeAPIVIew(APIView):
    """
        this api work for getting all Starline biding types
    """
    def get(self, request , format=None):
        bidding_type = MarketGameBiddingType.objects.filter(market_type = 1)
        serializer = MarketGameBiddingTypeSerializer(bidding_type , many =True)
        return Response(serializer.data)


class UserBiddingListAPIView(APIView):
    """
    Create a Bid in the .
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]


    def post(self, request, pk ,format=None):
        serializer = UserBiddingSerializer(data=request.data)
        # import pdb ; pdb.set_trace()
        user = User.objects.get(pk= pk) 
        if user.wallet_amount >= request.data['bidding_points']:
            if serializer.is_valid():
                serializer.save()
                user.wallet_amount = user.wallet_amount - serializer.data['bidding_points']
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        message = {"meesage" : "You have Insufficient Funds, Please add Funds."}
        return Response(message , status=status.HTTP_204_NO_CONTENT)



class SingleDigitUserBettingListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , pk , format =None):

        betting = UserBetting.objects.filter(user_id = pk  , 
                                            market_game_bidding_type_id = 1 )
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class MainJodiDigitUserBettingListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , pk , format =None):

        betting = UserBetting.objects.filter(user_id = pk , 
                                            market_type = 'main',
                                            market_game_bidding_type_id = 2)
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class SinglePattiUserBettingListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , pk , format =None):

        betting = UserBetting.objects.filter(user_id = pk , 
                                            market_game_bidding_type_id = 3)
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class DoublePattiUserBettingListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request ,pk, format =None):

        betting = UserBetting.objects.filter(user_id = pk, 
                                            market_game_bidding_type_id = 4)
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class TriplePattiUserBettingListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , pk , format =None):

        betting = UserBetting.objects.filter(user_id = pk , 
                                            market_game_bidding_type_id = 5)
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class DepositHistoryCreateListAPIView(APIView):
    """
    Create a Deposit history by the user .
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk , format=None):       
        serializer = DepositHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(pk= pk) 
            user.wallet_amount = user.wallet_amount + serializer.data['amount']
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawRequestCreateListAPIView(APIView):
    """
    Create a Withdraw request by the user .
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = WithdrawRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopWinnersMainListAPIView(APIView):
    """
    List all top winners of main games.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , format =None):
        date = datetime.now().date()
        betting = UserBetting.objects.filter(created_date__day = date.day,
                                market_type = 'main').annotate(max_amount = Max('bidding_points'
                                )).order_by('-max_amount')[:10]
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)


class TopWinnersStarLineListAPIView(APIView):
    """
    List all top winners of main games.
    """
    authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self , request , format =None):
        date = datetime.now().date()
        betting = UserBetting.objects.filter(created_date__day = date.day,
                                market_type = 'starline').annotate(max_amount = Max('bidding_points'
                                )).order_by('-max_amount')[:10]
        serializer = UserBiddingSerializer(betting , many = True)
        return Response(serializer.data)