from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_mysql.models import ListCharField

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
	Groups = models.CharField(max_length=18)

	Donor = models.ForeignKey(User,related_name='Donor',on_delete=models.CASCADE)

	#Receiver = models.ForeignKey(User,related_name='Receiver',on_delete=models.CASCADE)

	Receivers = ListCharField(
		base_field = models.CharField(max_length=18),
        size=10,
        max_length=(18 * 11),  # 18 * 10 character nominals, plus commas
        default = []
    )

	Description = models.CharField(max_length=50)

	Amount = models.IntegerField(default=0)

	Tag = models.CharField(max_length=15)

	Date = models.DateTimeField(auto_now=True)


#####################


# class Friends(models.Model):
# 	Friendof = models.ForeignKey(User,related_name='Friendof',on_delete=models.CASCADE)
# 	Friendslist = models.ManyToManyField(User,related_name='Friendslist')

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
	Tag = models.CharField(max_length=15,default="Others")
	Amount = models.IntegerField(default=0)
	Damount = models.IntegerField(default=0)
	Description = models.CharField(max_length=50)
	Group = models.CharField(max_length=18)
	Time1 = models.DateTimeField(auto_now_add=True)
	Time2 = models.DateTimeField(auto_now=True)


class notificationsModel(models.Model):
	Sender = models.ForeignKey(User,related_name='sender1',on_delete=models.CASCADE)
	Receiver = models.ForeignKey(User,related_name='Receiver2',on_delete=models.CASCADE)
	message = models.CharField(max_length=50)
	seen = models.IntegerField(default=0)
