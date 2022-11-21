from django.urls import path
from website.views import IndexPageView

app_name = 'website'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),

]