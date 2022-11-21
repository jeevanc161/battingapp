from django.http import Http404
from rest_framework import permissions ,generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login
from dashboard.models import(
    User, 
    Assets, 
    DepositHistory,
    DepositOffers ,
    WithdrawHistory,
    News, 
    WithdrawRequest ,
    TradHistory
    ) 

from .serializers import (
    UserSerializer, 
    RegisterSerializer, 
    AssetsSerializer,
    DepositHistorySerializer,
    DepositOfferSerializer,
    WithdrawHistorySerializer,
    WithdrawRequestSerializer,
    TradHistorySerializer,
    NewsSerializer,
)
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
 

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class UserProfileAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk , format=None):
        user = self.get_object(pk)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)
  


class AssertListAPIView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        assets = Assets.objects.all()
        serializer = AssetsSerializer(assets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssertDtailAPIView(APIView):
    """
    Retrieve, update or delete a assets instance.
    """
    def get_object(self, pk):
        try:
            return Assets.objects.get(pk=pk)
        except Assets.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        assets = self.get_object(pk)
        serializer = AssetsSerializer(assets)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        assets = self.get_object(pk)
        serializer = AssetsSerializer(assets, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        assets = self.get_object(pk)
        assets.delete()
        message = {"meesage" : "Assert Deleted successfully"}
        return Response(message , status=status.HTTP_204_NO_CONTENT)


class DepositHistoryAPIView(APIView):
    """
    List all Deposit History, or create a new Deposit History.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        try:
            deposit = DepositHistory.objects.all()
        except deposit.DoesNotExist:
            raise Http404
        
        serializer = DepositHistorySerializer(deposit, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepositHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositHistoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a Deposit History instance.
    """
    def get_object(self, pk):
        try:
            return DepositHistory.objects.get(pk=pk)
        except DepositHistory.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        deposit = self.get_object(pk)
        serializer = DepositHistorySerializer(deposit)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        deposit = self.get_object(pk)
        serializer = DepositHistorySerializer(deposit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        deposit = self.get_object(pk)
        deposit.delete()
        message = {"meesage" : "Deposit Entry Deleted successfully"}
        return Response(message , status=status.HTTP_204_NO_CONTENT)


class DepositOfferAPIView(APIView):
    """
    List all Deposit Offers, or create a new Deposit Offer.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        try:
            deposit = DepositOffers.objects.all()
        except deposit.DoesNotExist:
            raise Http404
        
        serializer = DepositOfferSerializer(deposit, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepositOfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositOfferDetailAPIView(APIView):
    """
    Retrieve, update or delete a Deposit Offer instance.
    """
    def get_object(self, pk):
        try:
            return DepositOffers.objects.get(pk=pk)
        except DepositOffers.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        deposit = self.get_object(pk)
        serializer = DepositOfferSerializer(deposit)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        deposit = self.get_object(pk)
        serializer = DepositOfferSerializer(deposit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        deposit = self.get_object(pk)
        deposit.delete()
        message = {"meesage" : "Offer Deleted successfully"}
        return Response(message , status=status.HTTP_204_NO_CONTENT)


class WithdrawHistoryAPIView(APIView):
    """
    List all Withdraw History, or create a new Withdraw by User.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        try:
            withdraw = WithdrawHistory.objects.all()
        except WithdrawHistory.DoesNotExist:
            raise Http404
        
        serializer = WithdrawHistorySerializer(withdraw, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WithdrawHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawHistoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a Withdraw History instance.
    """
    def get_object(self, pk):
        try:
            return WithdrawHistory.objects.get(pk=pk)
        except WithdrawHistory.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        withdraw = self.get_object(pk)
        serializer = WithdrawHistorySerializer(withdraw)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        withdraw = self.get_object(pk)
        serializer = WithdrawHistorySerializer(withdraw, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, pk, format=None):
    #     withdraw = self.get_object(pk)
    #     withdraw.delete()
    #     message = {"meesage" : "withdraw Deleted successfully"}
    #     return Response(message , status=status.HTTP_204_NO_CONTENT)


class WithdrawRequestAPIView(APIView):
    """
    List all Withdraw Request, or create a new Withdraw Request.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        withdraws = WithdrawRequest.objects.all()
        serializer = WithdrawRequestSerializer(withdraws, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WithdrawRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawRequestDetailAPIView(APIView):
    """
    Retrieve, update or delete a Withdraw request instance.
    """
    def get_object(self, pk):
        try:
            return WithdrawRequest.objects.get(pk=pk)
        except WithdrawRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        withdraw = self.get_object(pk)
        serializer = WithdrawRequestSerializer(withdraw)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        withdraw = self.get_object(pk)
        serializer = WithdrawRequestSerializer(withdraw, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        withdraw = self.get_object(pk)
        withdraw.delete()
        message = {"meesage" : "Withdraw Request successfully"}
        return Response(message , status=status.HTTP_204_NO_CONTENT)


class TradHistoryAPIView(APIView):
    """
    List all Trad History, or create a new Trad.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        trads = TradHistory.objects.all()
        serializer = TradHistorySerializer(trads, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TradHistorySerializer(data=request.data)
        import pdb; pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TradHistoryDtailAPIView(APIView):
    """
    Retrieve, update or delete a Trad instance.
    """
    def get_object(self, pk):
        try:
            return TradHistory.objects.get(pk=pk)
        except TradHistory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        trad = self.get_object(pk)
        serializer = TradHistorySerializer(trad)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        trad = self.get_object(pk)
        serializer = TradHistorySerializer(trad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        trad = self.get_object(pk)
        trad.delete()
        message = {"meesage" : "Assert Deleted successfully"}
        return Response(message , status=status.HTTP_204_NO_CONTENT)


class NewsAPIView(APIView):
    """
    List all News, or create a new News.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        news= News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDtailAPIView(APIView):
    """
    Retrieve, update or delete a News instance.
    """
    def get_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        news = self.get_object(pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        news = self.get_object(pk)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, pk, format=None):
    #     assets = self.get_object(pk)
    #     assets.delete()
    #     message = {"meesage" : "Assert Deleted successfully"}
    #     return Response(message , status=status.HTTP_204_NO_CONTENT)