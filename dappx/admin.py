# from django.contrib import admin
# from dappx.models import UserProfile, User
# # Register your models here.

# admin.site.register(UserProfile)

from django.contrib import admin
from dappx.models import UserProfileInfo, User, Transaction, Friends, ftoftransaction, GroupsModel, notificationsModel,Activity
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Transaction)
admin.site.register(Friends)
admin.site.register(ftoftransaction)
admin.site.register(GroupsModel)
admin.site.register(notificationsModel)
admin.site.register(Activity)