import csv
import calendar
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render , redirect , reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic 
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from knox.models import AuthToken
from django.db.models import Sum , Count
from .models import ( User , Assets , DepositHistory , News , DepositOffers , WithdrawHistory, 
                        WithdrawRequest , TradHistory)
from .form import ( UserForm , UserCreateForm , AssetsFrom  , DepositHistoryForm , NewsForm , 
                    DepositOfferForm , WithdrawHistoryForm , WithdrawRequestForm , TradHistoryForm )

from .utils import render_to_pdf # FOR PDF EXPORT
from django.template.loader import get_template #FOR PDF EXPORT

class AdminIndexPageView(LoginRequiredMixin, generic.TemplateView):
    """
        Get Admin Dashboard Page View and display Data
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        month = []
        users = [] 
        context = super(AdminIndexPageView, self).get_context_data(**kwargs)
        user = self.request.user
        total_users = User.objects.filter(is_staff = 0).count()
        active_users = User.objects.filter(is_active = 1).count()
        total_deposit = DepositHistory.objects.aggregate(Sum('amount'))
        total_bounus = User.objects.aggregate(Sum('total_bonus_amount'))
        total_withdraw = WithdrawHistory.objects.aggregate(Sum('amount'))
        total_assets = Assets.objects.all().count()
        total_trad = TradHistory.objects.all().count()
        deposit_historys = DepositHistory.objects.filter(transaction_date__month = datetime.today().month).order_by('-transaction_date')
        total_month_users = User.objects.filter().extra({'month':"Extract(month from account_created_date)"}).values_list('month').annotate(Count('id')).order_by('month')
        for entry in total_month_users:
            month.append(calendar.month_name[entry[0]])
            users.append(entry[1]) 

        context.update({
            'total_users': total_users,
            'active_users' : active_users,
            'total_deposit' : total_deposit['amount__sum'],
            'total_bounus' : total_bounus['total_bonus_amount__sum'],
            'total_withdraw' : total_withdraw['amount__sum'],
            'total_assets' : total_assets,
            'total_trad': total_trad,
            'deposit_historys' : deposit_historys,
            'month' : month,
            'users': users

        })
        return context



class UserListPageView(LoginRequiredMixin , generic.ListView):
    """
        User List Page view for display all the Users 
    """
    template_name = 'dashboard/users.html'
    context_object_name  = 'users'

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        if 'search_name' in self.request.GET:
            search_name = self.request.GET['search_name']
            queryset = User.objects.filter(username__icontains = search_name)
        else:
            queryset = User.objects.all().order_by('-account_created_date')
        return queryset


class UserDetailPageView(LoginRequiredMixin, generic.DetailView):
    """
        Display a user complate data
    """
    template_name = 'dashboard/user_detail.html'
    context_object_name  = 'user' 

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class UserDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a user and redirect to the User List View
    """
    url = '/admin/list_user'  
    success_message = 'Profile successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        AuthToken.objects.filter(user_id = del_id).delete()
        User.objects.get(id = del_id).delete()
        # messages.success(request,"User Removed!!!")
        return super().get_redirect_url(*args , **kwargs)


class UserUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the user data and and display a success message to the admin side
    """
    template_name = 'dashboard/user_update.html'
    form_class = UserForm
    success_message = 'Profile successfully Updated!!!!'

    def get_queryset(self):
        return User.objects.all()

    def get_success_url(self):
        # messages.success(request,"Profile Updated!")
        return reverse('dashboard:user_update' , kwargs = {'pk': self.get_object().id})


class UserCreatePageView(LoginRequiredMixin ,  SuccessMessageMixin, generic.CreateView):
    """
        Create the New user and and display the user into the user list view
    """
    template_name = 'dashboard/user_create.html'
    form_class = UserCreateForm
    success_message = 'Profile successfully Created!!!!'

    def get_success_url(self):
        return reverse('dashboard:user_list')

    def form_valid(self, form):
        user  = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super(UserCreatePageView , self).form_valid(form)


class AssertListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Assert List and render to the assert List view in admin site
    """
    template_name = 'dashboard/assets_list.html'
    # paginate_by = 10
    context_object_name = 'assets'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = Assets.objects.filter(name__icontains = name)
        else:
            queryset = Assets.objects.all()

        return queryset


class AssertCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a Assert with this class based view
    """

    template_name = 'dashboard/assets_create.html'
    form_class = AssetsFrom
    success_message = "Aserts Created successfully!!!!"

    def get_success_url(self):
        return reverse('dashboard:assets_list')

    def form_valid(self, form):
        form.save()
        return super(AssertCreatePageView , self).form_valid(form)


class AssetsDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Assets and redirect to the Asset List View
    """
    url = '/admin/assets'  
    success_message = 'Assets successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        Assets.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)


class AssetsUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Assets data and and display a success message to the admin side
    """
    template_name = 'dashboard/assets_update.html'
    form_class = AssetsFrom
    success_message = 'Assets successfully Updated!!!!'

    def get_queryset(self):
        return Assets.objects.all()

    def get_success_url(self):
        return reverse('dashboard:assets_update' , kwargs = {'pk': self.get_object().id})


class AssetsDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the assets data
    '''
    template_name = 'dashboard/assets_detail.html'
    context_object_name = 'assets'

    def get_queryset(self):
        queryset = Assets.objects.all()
        return queryset


class DepositHistoryListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Deposit History List and render to the assert List view in admin site
    """
    template_name = 'dashboard/deposit_history_list.html'
    # paginate_by = 10
    context_object_name = 'deposit_historys'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = DepositHistory.objects.filter(user_id__first_name__icontains = name)
        else:
            queryset = DepositHistory.objects.all().order_by('-transaction_date')
        return queryset


class DepositHistoryDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the Deposit History  data
    '''
    template_name = 'dashboard/deposit_history_detail.html'
    context_object_name = 'deposit_history'

    def get_queryset(self):
        queryset = DepositHistory.objects.all()
        return queryset


class DepositHistoryUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Diposit History data and and display a success message to the admin side
    """
    template_name = 'dashboard/deposit_history_update.html'
    form_class = DepositHistoryForm
    success_message = 'Deposit History successfully Updated!!!!'

    def get_queryset(self):
        return DepositHistory.objects.all()

    def get_success_url(self):
        return reverse('dashboard:deposit_history_update' , kwargs = {'pk': self.get_object().id})


class DepositHistoryCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a Deposit History with this class based view
    """

    template_name = 'dashboard/deposit_history_create.html'
    form_class = DepositHistoryForm
    success_message = "Deposit History Created successfully!!!!"

    def get_success_url(self):
        return reverse('dashboard:deposit_history_list')

    def form_valid(self, form):
        form.save()
        return super(DepositHistoryCreatePageView , self).form_valid(form)


class DepositHistoryDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Deposit History and redirect to the Asset List View
    """
    url = '/admin/deposit_history'  
    success_message = 'Deposit History successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        DepositHistory.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)


class NewsListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the News List and render to the assert List view in admin site
    """
    template_name = 'dashboard/news_list.html'
    # paginate_by = 10
    context_object_name = 'news'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = News.objects.filter(name__icontains = name)
        else:
            queryset = News.objects.all().order_by('-date')
        return queryset


class NewsCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a News with this class based view
    """

    template_name = 'dashboard/news_create.html'
    form_class = NewsForm
    success_message = "News Created successfully!!!!"

    def get_success_url(self):
        return reverse('dashboard:news_list')

    def form_valid(self, form):
        form.save()
        return super(NewsCreatePageView , self).form_valid(form)


class NewsDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a News and redirect to the Asset List View
    """
    url = '/admin/news/'  
    success_message = 'News successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        News.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)


class NewsDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the News  data
    '''
    template_name = 'dashboard/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = News.objects.all()
        return queryset


class NewsUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the news data and and display a success message to the admin side
    """
    template_name = 'dashboard/news_update.html'
    form_class = NewsForm
    success_message = 'News successfully Updated!!!!'

    def get_queryset(self):
        return News.objects.all()

    def get_success_url(self):
        return reverse('dashboard:news_update' , kwargs = {'pk': self.get_object().id})
        

class DepositOfferListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Deposit Offer List and render to the assert List view in admin site
    """
    template_name = 'dashboard/deposit_offer_list.html'
    # paginate_by = 10
    context_object_name = 'deposit_offers'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = DepositOffers.objects.filter(name__icontains = name)
        else:
            queryset = DepositOffers.objects.all().order_by('-date')
        return queryset


class DepositOfferCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a Deposit Offer with this class based view
    """

    template_name = 'dashboard/deposit_offer_create.html'
    form_class = DepositOfferForm
    success_message = "Offer Created successfully!!!!"

    def get_success_url(self):
        return reverse('dashboard:deposit_offer_list')

    def form_valid(self, form):
        form.save()
        return super(DepositOfferCreatePageView , self).form_valid(form)


class DepositOfferDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the Deposit Offer data
    '''
    template_name = 'dashboard/deposit_offer_detail.html'
    context_object_name = 'deposit_offer'

    def get_queryset(self):
        queryset = DepositOffers.objects.all()
        return queryset


class DepositOfferUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Deposit Offer data and and display a success message to the admin side
    """
    template_name = 'dashboard/deposit_offer_update.html'
    form_class = DepositOfferForm
    success_message = 'Offer successfully Updated!!!!'

    def get_queryset(self):
        return DepositOffers.objects.all()

    def get_success_url(self):
        return reverse('dashboard:deposit_offer_update' , kwargs = {'pk': self.get_object().id})


class DepositOfferDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Deposit Offer and redirect to the Asset List View
    """
    url = '/admin/deposit_offer/'  
    success_message = 'Offer successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        DepositOffers.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)   


class WithdrawHistoryListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Withdraw Histroy List and render to the Widhdraw History List view in admin site
    """
    template_name = 'dashboard/withdrow_history_list.html'
    # paginate_by = 10
    context_object_name = 'withdraw_historys'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = WithdrawHistory.objects.filter(user_id__first_name__icontains = name)
        else:
            queryset = WithdrawHistory.objects.all().order_by('-transaction_date')
        return queryset


class WithdrawHistoryCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a  Withdraw Histroy with this class based view
    """

    template_name = 'dashboard/withdrow_history_create.html'
    form_class = WithdrawHistoryForm
    success_message = "Withdraw History Created successfully!!!!"

    def get_success_url(self):
        return reverse('dashboard:withdraw_history_list')

    def form_valid(self, form):
        form.save()
        return super(WithdrawHistoryCreatePageView ,self).form_valid(form)


class WithdrawHistoryDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the Withdraw History data
    '''
    template_name = 'dashboard/withdraw_history_detail.html'
    context_object_name = 'withdraw_history'

    def get_queryset(self):
        queryset = WithdrawHistory.objects.all()
        return queryset


class WithdrawHistoryUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Withdraw History data and and display a success message to the admin side
    """
    template_name = 'dashboard/withdraw_history_update.html'
    form_class = WithdrawHistoryForm
    success_message = 'Withdrow History successfully Updated!!!!'

    def get_queryset(self):
        return WithdrawHistory.objects.all()

    def get_success_url(self):
        return reverse('dashboard:withdraw_history_update' , kwargs = {'pk': self.get_object().id})


class WithdrawHistoryDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Deposit Offer and redirect to the Asset List View
    """
    url = '/admin/withdraw_history/'  
    success_message = 'Offer successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        WithdrawHistory.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)   



class WithdrawRequestListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Withdraw Request List and render to the Widhdraw History List view in admin site
    """
    template_name = 'dashboard/withdrow_request_list.html'
    # paginate_by = 10
    context_object_name = 'withdraw_requests'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = WithdrawRequest.objects.filter(user_id__first_name__icontains = name)
        else:
            queryset = WithdrawRequest.objects.all().order_by('-date_time')
        return queryset


class WithdrawRequestCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a  Withdraw Request with this class based view
    """

    template_name = 'dashboard/withdrow_request_create.html'
    form_class = WithdrawRequestForm
    success_message = "Withdraw Request Created !!!!"

    def get_success_url(self):
        return reverse('dashboard:withdraw_request_list')

    def form_valid(self, form):
        form.save()
        return super(WithdrawRequestCreatePageView ,self).form_valid(form)


class WithdrawRequestDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the Withdraw Request data
    '''
    template_name = 'dashboard/withdraw_request_detail.html'
    context_object_name = 'withdraw_request'

    def get_queryset(self):
        queryset = WithdrawRequest.objects.all()
        return queryset


class WithdrawRequestUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Withdraw Request data and and display a success message to the admin side
    """
    template_name = 'dashboard/withdraw_request_update.html'
    form_class = WithdrawRequestForm
    success_message = 'Withdrow Request successfully Updated!!!!'

    def get_queryset(self):
        return WithdrawRequest.objects.all()

    def get_success_url(self):
        return reverse('dashboard:withdraw_request_update' , kwargs = {'pk': self.get_object().id})


class WithdrawRequestDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Withdraw Requestand redirect to the Withdraw Request List View
    """
    url = '/admin/withdraw_request/'  
    success_message = 'Request successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        WithdrawRequest.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)   


class TradHistoryListPageView(LoginRequiredMixin , generic.ListView):
    """
        Get all the Trad History List and render to the Widhdraw History List view in admin site
    """
    template_name = 'dashboard/trad_history_list.html'
    # paginate_by = 10
    context_object_name = 'trad_historys'

    def get_queryset(self):
        if 'search' in self.request.GET:
            name = self.request.GET['search']
            queryset = TradHistory.objects.filter(user_id__first_name__icontains = name)
        else:
            queryset = TradHistory.objects.all().order_by('-date')
        return queryset


class TradHistoryCreatePageView(LoginRequiredMixin, SuccessMessageMixin , generic.CreateView):
    """
        Create a  Trad History  with this class based view
    """

    template_name = 'dashboard/trad_history_create.html'
    form_class = TradHistoryForm
    success_message = "Trad Hisotry Created !!!!"

    def get_success_url(self):
        return reverse('dashboard:trad_history_list')

    def form_valid(self, form):
        form.save()
        return super(TradHistoryCreatePageView ,self).form_valid(form)


class TradHistoryDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the Trad History data
    '''
    template_name = 'dashboard/trad_history_detail.html'
    context_object_name = 'trad_history'

    def get_queryset(self):
        queryset = TradHistory.objects.all()
        return queryset


class TradHistoryUpdatePageView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    """
        Update the Trad History data and and display a success message to the admin side
    """
    template_name = 'dashboard/trad_history_update.html'
    form_class = TradHistoryForm
    success_message = 'Trad History successfully Updated!!!!'

    def get_queryset(self):
        return TradHistory.objects.all()

    def get_success_url(self):
        return reverse('dashboard:trad_history_update' , kwargs = {'pk': self.get_object().id})



class TradHistoryDeletePageView(LoginRequiredMixin, SuccessMessageMixin, generic.RedirectView): 
    """
        Delete a Trad History record redirect to the Trad history List View
    """
    url = '/admin/trad_history/'  
    success_message = 'Resource successfully Deleted!!!!'

    def get_redirect_url(self , *args , **kwargs):
        del_id = kwargs['id']
        TradHistory.objects.get(id = del_id).delete()
        return super().get_redirect_url(*args , **kwargs)  

class UserDocumentPageView(LoginRequiredMixin , generic.DetailView):

    '''
        Detail view for the Trad Document data
    '''
    template_name = 'dashboard/user_document_detail.html'
    context_object_name = 'user_document'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class UserDepositHistoryPageView(LoginRequiredMixin , generic.ListView):

    '''
        Detail view for the Trad Document data
    '''
    template_name = 'dashboard/user_deposit_history_detail.html'
    context_object_name = 'user_deposit_history'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = DepositHistory.objects.filter(user_id = pk).order_by('-transaction_date')
        return queryset

    def get_context_data(self, **kwargs):
        context =  super(UserDepositHistoryPageView , self).get_context_data(**kwargs)
        context.update({
            'pk' : self.kwargs['pk'] , 
        })
        return context


class UserWithdrawHistoryPageView(LoginRequiredMixin , generic.ListView):

    '''
        Detail view for the Trad Document data
    '''
    template_name = 'dashboard/user_withdraw_history_detail.html'
    context_object_name = 'user_withdraw_history'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = WithdrawHistory.objects.filter(user_id = pk).order_by('-transaction_date')
        return queryset

    def get_context_data(self, **kwargs):
        context =  super(UserWithdrawHistoryPageView , self).get_context_data(**kwargs)
        context.update({
            'pk' : self.kwargs['pk'] , 
        })
        return context


class UserAccountDetailPageView(LoginRequiredMixin , generic.DetailView):
    '''
        Detail view for the User account details 
    '''
    template_name = 'dashboard/user_account_detail.html'
    context_object_name = 'user_account'

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


def csv_user_write(request):
    """
        Export User details in the CSV file using a function based view
    """

    users  = User.objects.all().order_by('-account_created_date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username' , 'Email', 'First Name', 'Middle Name', 'Last Name', 
                       'Phone Number', 'Date Of Birth' , 'Country' , 'City' , 'Account Created Date'
                       , 'Bank Account Number' , 'Bank Name' , 'Ifsc Code' , 'Wallet Amount',
                       'Total Bonus Amount', 'Account Opening Bonus'])
    for user in users:
        writer.writerow([user.username , user.email , user.first_name, user.middle_name, user.last_name, 
                        user.phone_number, user.dob , user.country , user.city , user.account_created_date ,
                        user.bank_account_number , user.bank_name , user.ifsc_code , user.wallet_amount ,
                        user.total_bonus_amount , user.account_opening_bonus])

    return response


def pdf_user_view(request, *args, **kwargs):   #FOR PDF EXPORT
    template = get_template('dashboard/user_pdf_template.html')
    users = User.objects.all().order_by('-account_created_date')
    context = {'users':users}
    html  = template.render(context)
    pdf  = render_to_pdf('dashboard/user_pdf_template.html', context)
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf') # TILL HERE HTML TO PDF 
    return HttpResponse("Not found")