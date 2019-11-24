from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django_mysql.models import ListCharField
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# Create your models here.

#####################
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	nickname = models.CharField(max_length=15,default='SOME STRING')

	portfolio_site = models.URLField(blank=True)

	profile_pic = models.ImageField(upload_to='profile_pics',default='profile.jpg')

	def __str__(self):
		return self.user.username

######################


class Transaction(models.Model):
	Groups = models.CharField(max_length=20)

	Donor = models.ForeignKey(User,related_name='Donor',on_delete=models.CASCADE)

	#Receiver = models.ForeignKey(User,related_name='Receiver',on_delete=models.CASCADE)

	Receivers = ListCharField(
		base_field = models.CharField(max_length=18),
        size=10,
        max_length=(18 * 11),  # 18 * 10 character nominals, plus commas
        default = []
    )

	Description = models.CharField(max_length=50)

	Amount = models.DecimalField(default=0,max_digits=12, decimal_places=3)

	# SplitAmount = models.ListCharField(
	# 	base_field = models.FloatField(max_length=18),
 #        size=10,
 #        max_length=(18 * 11),  # 18 * 10 character nominals, plus commas
 #        default = []
 #    )

	Tag = models.CharField(max_length=15)

	Date = models.DateTimeField(auto_now_add=True)
	Date2 = models.CharField(default=date.today().strftime('%Y-%m-%d'),max_length=25)
	Expenditure = models.FloatField(default=0)


#####################

class Friends(models.Model):
	Friendslist = models.ManyToManyField(User) 
	current_user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE,null=True)

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friends, created =cls.objects.get_or_create(
			current_user=current_user
		)
		friends.Friendslist.add(new_friend)

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friends, created =cls.objects.get_or_create(
			current_user=current_user
		)
		friends.Friendslist.remove(new_friend)

class ftoftransaction(models.Model):
	Donor = models.ForeignKey(User,related_name='Donor1',on_delete=models.CASCADE)
	Receiver = models.ForeignKey(User,related_name='Receiver1',on_delete=models.CASCADE)
	Amount = models.DecimalField(default=0,max_digits=12, decimal_places=3)
	Damount = models.DecimalField(default=0,max_digits=12, decimal_places=3)
	Description = models.CharField(max_length=50)
	Group = models.CharField(max_length=20)
	Tag = models.CharField(max_length=15,default="Others")
	Time1 = models.DateTimeField(auto_now_add=True)
	Time2 = models.DateTimeField(auto_now=True)
	Date2 = models.CharField(default=date.today().strftime('%Y-%m-%d'),max_length=25)

class GroupsModel(models.Model):
	Group = models.CharField(max_length=20)
	Member = models.ForeignKey(User,related_name='Member',on_delete=models.CASCADE)
	Amount = models.DecimalField(default=0,max_digits=12, decimal_places=3)
	Damount = models.DecimalField(default=0,max_digits=12, decimal_places=3)
	Description = models.CharField(max_length=50)
	Tag = models.CharField(max_length=15,default="Others")
	in_group = models.BooleanField(default=True)

class notificationsModel(models.Model):
	Sender = models.ForeignKey(User,related_name='sender1',on_delete=models.CASCADE)
	Receiver = models.ForeignKey(User,related_name='Receiver2',on_delete=models.CASCADE)
	message = models.CharField(max_length=50)
	seen = models.IntegerField(default=0)

class Activity(models.Model):
	Button_name = models.CharField(max_length=25)
	Group_name = models.CharField(max_length=20)
	Donor = models.CharField(max_length=20)
	Receivers_list = models.CharField(max_length=200)
	Amount = models.DecimalField(default=0,max_digits=12, decimal_places=3)
	Description = models.CharField(max_length=50)
	Time = models.DateTimeField(auto_now_add=True)
	Tag = models.CharField(max_length=15,default="other")