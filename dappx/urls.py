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
    url(r'^Transactions_unequal/$', views.Transactions_unequal, name='Transactions_unequal'),
    url(r'^Transactions_unequal_actual/(?P<operation>.+)/(?P<groupname>.+)/$', views.Transactions_unequal_actual, name='Transactions_unequal_actual'),
    url(r'^Transactions_unequal_extended/$', views.Transactions_unequal_extended, name='Transactions_unequal_extended'),
    url(r'^Transactions/$', views.Transactions, name='Transactions'),
    url(r'^group_transactions/$', views.group_transactions, name='group_transactions'),
    url(r'^friend_transaction/$', views.friend_transaction, name='friend_transaction'),
    url(r'^addfriends/$', views.addfriends, name='addfriends'),
    #url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^creategroup/$', views.creategroup, name='creategroup'),
    url(r'^view_friend/(?P<pk>\d+)/$', views.view_friend, name='view_friend'),
    url(r'^view_group/(?P<operation>.+)/$', views.view_group, name='view_group'),
    url(r'^settle_up/(?P<pk>\d+)/$', views.settle_up, name='settle_up'),
    url(r'^settle_up_in_group/(?P<operation>.+)/(?P<pk>\d+)/$', views.settle_up_in_group, name='settle_up_in_group'),
    url(r'^Leave_group/(?P<operation1>.+)/$', views.Leave_group, name='Leave_group'),
    url(r'^notifications/$',views.notifications,name='Notifications'),
    url(r'^activity/$',views.activity,name='activity'),
    url(r'^send_notification/(?P<pk>\d+)/$',views.send_notification,name='send_notification'),
    url(r'^time_series_plots/$',views.time_series_plots,name='time_series_plots'),
    url(r'^tagplots/$',views.tagplots,name='tagplots')
    # url(r'^ftoftransaction/$',views.ftoftransaction, name='ftoftransaction')
]