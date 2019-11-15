# dappx/urls.py

from django.conf.urls import url
from dappx import views
# SET THE NAMESPACE!
app_name = 'dappx'

# Be careful setting the name to just /login use userlogin instead!

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^change_pic/$',views.update_pic,name='update_pic'),
    url(r'^password/$', views.Reset, name='Reset'),
    url(r'^change_pic/$',views.update_pic,name='update_pic'),
    url(r'^Friends/$', views.Friendstab, name='Friendstab'),
    url(r'^Groups/$', views.Groups, name='Groups'),
    url(r'^Transactions/$', views.Transactions, name='Transactions'),
    url(r'^addfriends/$', views.addfriends, name='addfriends'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
]