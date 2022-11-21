from django.db import models
from dashboard.models import User
from datetime import datetime

class Notification(models.Model):
	"""
		Model class for the Notification table Stucture
	"""

	title  				= models.CharField(max_length=250)
	description 		= models.TextField()
	created_date  		= models.DateTimeField(auto_now_add = True)
	Updated_date  		= models.DateTimeField(auto_now = True)


	def __str__(self):
		return self.title


WITHDROW_HISTORY_STATUS = [
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),
            ]
class WithdrawHistory(models.Model):
    '''
        Model class for managing the WithDraw Histroy of the Batting Application
    '''

    user_id                 = models.ForeignKey(User , related_name='withdraw_created' ,on_delete=models.CASCADE)
    transaction_date        = models.DateTimeField(auto_now_add=True)
    transaction_time        = models.TimeField(auto_now_add = True)
    amount                  = models.FloatField(default = 0.0)
    payment_id              = models.CharField(max_length= 250)
    payment_mode            = models.CharField(max_length=250)
    payment_source          = models.CharField(max_length = 250)
    status                  = models.IntegerField(choices = WITHDROW_HISTORY_STATUS , default = 0)
    remarks                 = models.TextField()

    def __str__(self):
        return self.user_id.username




WITHDROW_STATUS = [
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),

            ]

class WithdrawRequest(models.Model):
    '''
        Model class for managing the Withdraw Request of the betting Application
    '''

    user_id                 = models.ForeignKey(User ,related_name='withdraw_request_created' , on_delete=models.CASCADE)
    request_amount          = models.FloatField(default=0.0)
    date_time               = models.DateTimeField(auto_now_add= True)
    status                  = models.SmallIntegerField(choices= WITHDROW_STATUS, default = 0)

    def __str__(self):
        return self.user_id.username



DEPOSIT_STATUS = [ # pending , success decline
                (0, 'Pending'), 
                (1, 'Success'),
                (2 , 'Decline'),
            ] 

class DepositHistory(models.Model):
    '''
        Model class for managing the Deposit History of the User
    '''

    user_id                 = models.ForeignKey(User ,related_name='deposit_created' ,on_delete=models.CASCADE)
    transaction_date        = models.DateTimeField(auto_now_add=True)
    transaction_time        = models.TimeField(auto_now_add=True )
    amount                  = models.FloatField(default=0.0)
    bonus_amount            = models.FloatField()
    payment_id              = models.CharField(max_length= 250)
    payment_mode            = models.CharField(max_length=250)
    payment_source          = models.CharField(max_length = 250)
    status                  = models.IntegerField(choices = DEPOSIT_STATUS , default = 0)

    def __str__(self):
        return self.user_id.username


MARKET_TYPE = [ 
            (0 , 'Main'),
            (1 , 'Star Line') 
            ]

class GamePrice(models.Model):

    '''
        Model class for managing the main game price of the User
    '''

    name 				= models.CharField(max_length = 250)
    market_type         = models.IntegerField(choices = MARKET_TYPE ,  default = 0)
    bet_amount  		= models.FloatField()
    win_amount  		= models.FloatField()
    created_date  		= models.DateTimeField(auto_now_add = True)
    updated_date  		= models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name


# class TopWinner(models.Model):
#     '''
#         Model class for managing the top winners for the betting applcaion
#     '''

#     name   			     = models.CharField(max_length = 250)
#     market_category      = models.IntegerField(choices = MARKET_CATEGORY ,  default = 0)
#     digit  			     = models.FloatField()
#     win_amount    	     = models.FloatField()
#     game_name  		     = models.CharField(max_length = 250)
#     date_time 		     = models.DateTimeField(auto_now_add = True)


MARKET_STATUS = [
                (0 , "Open"),
                (1 , "Closed" )
                ]
GAME_TYPE  = [
                (0 ,"OPEN"),
                (1 , "CLOSE")

            ]
GAME_STATUS = [
                (0 , "Betting is Closed For Today"),
                (1 , "Batting is Running Now")
            ]

class MarketGame(models.Model):
    """
        Model Class For the Market Game fo the Betting
    """

    name                    = models.CharField(max_length = 250)
    market_type             = models.IntegerField(choices =  MARKET_TYPE, default = 0) 
    # digit                   = models.CharField(max_length = 250 ,blank =True , null = True)
    # date                    = models.DateTimeField()
    game_type               = models.CharField(max_length = 250 , default = 0)
    game_type_open          = models.CharField(max_length = 250 , default = 'open')
    game_type_close         = models.CharField(max_length = 250  , default = 'close')
    open_time               = models.TimeField(blank =True , null = True)
    close_time              = models.TimeField(blank =True , null = True)
    open_result_time        = models.TimeField(blank =True , null = True)
    close_result_time       = models.TimeField(blank =True , null = True)
    open_single_result      = models.CharField(max_length= 250 ,blank =True , null = True)
    open_triple_result      = models.CharField(max_length = 250 , blank =True , null = True)
    close_single_result     = models.CharField(max_length = 250 , blank =True , null = True)
    close_triple_result     = models.CharField(max_length = 250, blank =True , null = True)
    close_jodi_result       = models.CharField(max_length = 250, blank =True , null = True)
    status                  = models.IntegerField(choices = GAME_STATUS)
    created_date            = models.DateTimeField(auto_now_add =True )
    updated_date            = models.DateTimeField(auto_now =True )


# class StarLineGame(models.Model):
#     """
#         Star Line game model class 
#     """

#     name = models.CharField(max_length = 250 , default = "Starline Games")
#     time = models.TimeField()
#     result_digit = models.CharField(max_length = 250)
#     status = models.IntegerField(default = GAME_STATUS , blank =True , null = True)


class MarketGameBiddingType(models.Model):
    """
        This class is user for the type of Bidding in the application 
        like - single digit
                Panna
                single Patti etc
    """

    name        = models.CharField(max_length=250)
    market_type = models.IntegerField(choices = MARKET_TYPE , default = 0)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)



class UserBetting(models.Model):
    """
        This is the table for managing the details of the each market bidding 
    """

    user_id                     = models.ForeignKey(User , on_delete=models.CASCADE)
    market_id                   = models.ForeignKey(MarketGame , on_delete = models.CASCADE)
    market_game_bidding_type_id = models.ForeignKey(MarketGameBiddingType , related_name = 'bidding_game_bid_type' , on_delete = models.CASCADE)
    market_type                 = models.CharField(max_length = 250) # (Star Line / Noramal )
    game_category               = models.CharField(max_length = 250) # category (open / Close )
    bidding_digit               = models.CharField(max_length = 250)
    bidding_points              = models.FloatField(default = 0.0)
    bidding_date                = models.DateTimeField(default = datetime.now)
    bidding_time                = models.TimeField(auto_now_add = True)
    created_date                = models.DateTimeField(auto_now_add =True)
    updated_date                = models.DateTimeField(auto_now = True)


class UserWinner(models.Model):
    """
        This is the table where we can manage the all Winner user who won the Betting
    """
    user_bidding_id             = models.OneToOneField(UserBetting , on_delete=models.CASCADE)
    user_id                     = models.ForeignKey(User , related_name = 'winner_user', on_delete= models.CASCADE)
    market_id                   = models.ForeignKey(MarketGame , related_name = 'winner_market_game' , on_delete = models.CASCADE)
    market_game_bidding_type_id = models.ForeignKey(MarketGameBiddingType , related_name = 'winner_game_bid_type' , on_delete = models.CASCADE)
    market_type                 = models.CharField(max_length = 250) # (Star Line / Noramal )
    game_category               = models.CharField(max_length = 250) # category (open / Close )
    bidding_digit               = models.CharField(max_length = 250)
    win_bidding_digit           = models.IntegerField(default = 0)
    bidding_points              = models.FloatField(default = 0.0)
    bidding_date                = models.DateTimeField(default = datetime.now)
    bidding_time                = models.TimeField(auto_now_add = True)
    created_date                = models.DateTimeField(auto_now_add =True)
    updated_date                = models.DateTimeField(auto_now = True)

class DigitNumberHistroy(models.Model):
    """
        Market digit histroy 
    """
    market_id               = models.ForeignKey(MarketGame , related_name = 'history_market_game' , on_delete = models.CASCADE)
    market_type             = models.CharField(max_length = 250) # (Star Line / Noramal )
    open_single_result      = models.CharField(max_length= 250 ,blank =True , null = True)
    open_triple_result      = models.CharField(max_length = 250 , blank =True , null = True)
    close_single_result     = models.CharField(max_length = 250 , blank =True , null = True)
    close_triple_result     = models.CharField(max_length = 250, blank =True , null = True)
    close_jodi_result       = models.CharField(max_length = 250, blank =True , null = True)
    created_date            = models.DateTimeField(auto_now_add = True)



# class SingleDigitBetting(models.Model):
#     """
#         Model Class for the Single Digit Betting 
#     """

#     user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
#     game_price_id           = models.ForeignKey(GamePrice , on_delete = models.CASCADE)
#     market_id               = models.ForeignKey(MarketGame , on_delete = models.CASCADE)
#     martet_category         = models.IntegerField(choices = MARKET_CATEGORY)
#     market_game_type        = models.IntegerField(choices = GAME_TYPE)
#     points                  = models.CharField(max_length = 250)
#     digit                   = models.CharField(max_length = 250)
#     date                    = models.DateTimeField()
#     time                    = models.TimeField()
#     status                  = models.IntegerField(choices = MARKET_STATUS)


# class JodiBetting(models.Model):
#     """
#         Model Class for the Jodi Betting 
#     """

#     user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
#     game_price_id           = models.ForeignKey(GamePrice , on_delete = models.CASCADE)
#     market_id               = models.ForeignKey(MarketGame , blank=True , null=True, on_delete=models.SET_NULL)
#     star_line_id            = models.ForeignKey(StarLineGame , blank=True , null=True, on_delete=models.SET_NULL)
#     martet_category         = models.IntegerField(choices = MARKET_CATEGORY)
#     market_game_type        = models.IntegerField(choices = GAME_TYPE)
#     points                  = models.CharField(max_length = 250)
#     digit                   = models.CharField(max_length = 250)
#     date                    = models.DateTimeField()
#     time                    = models.TimeField()
#     status                  = models.IntegerField(choices = MARKET_STATUS)


# class SinglePattiBetting(models.Model):
#     """
#         Model Class for the Jodi Betting 
#     """

#     user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
#     game_price_id           = models.ForeignKey(GamePrice , on_delete = models.CASCADE)
#     market_id               = models.ForeignKey(MarketGame , on_delete = models.CASCADE)
#     martet_category         = models.IntegerField(choices = MARKET_CATEGORY)
#     market_game_type        = models.IntegerField(choices = GAME_TYPE)
#     points                  = models.CharField(max_length = 250)
#     digit                   = models.CharField(max_length = 250)
#     date                    = models.DateTimeField()
#     time                    = models.TimeField()
#     status                  = models.IntegerField(choices = MARKET_STATUS)


# class DoublePattiBetting(models.Model):
#     """
#         Model Class for the Jodi Betting 
#     """

#     user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
#     game_price_id           = models.ForeignKey(GamePrice , on_delete = models.CASCADE)
#     market_id               = models.ForeignKey(MarketGame , on_delete = models.CASCADE)
#     martet_category         = models.IntegerField(choices = MARKET_CATEGORY)
#     market_game_type        = models.IntegerField(choices = GAME_TYPE)
#     points                  = models.CharField(max_length = 250)
#     digit                   = models.CharField(max_length = 250)
#     date                    = models.DateTimeField()
#     time                    = models.TimeField()
#     status                  = models.IntegerField(choices = MARKET_STATUS)


# class TriplePattiBetting(models.Model):
#     """
#         Model Class for the Jodi Betting 
#     """

#     user_id                 = models.ForeignKey(User , on_delete=models.CASCADE)
#     game_price_id           = models.ForeignKey(GamePrice , on_delete = models.CASCADE)
#     market_id               = models.ForeignKey(MarketGame , on_delete = models.CASCADE)
#     martet_category         = models.IntegerField(choices = MARKET_CATEGORY)
#     market_game_type        = models.IntegerField(choices = GAME_TYPE)
#     points                  = models.CharField(max_length = 250)
#     digit                   = models.CharField(max_length = 250)
#     date                    = models.DateTimeField()
#     time                    = models.TimeField()
#     status                  = models.IntegerField(choices = MARKET_STATUS)