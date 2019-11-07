from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class UserProfile(models.Model):
	
# 	user = models.OneToOneField(User,on_delete=models.CASCADE)
# 	#userid = models.CharField(max_length=10)
# 	portfolio_site = models.URLField(blank=True)

# 	userid = models.CharField(max_length=30)

# 	profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

# def __str__(self):
# 	return self.userid

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfileInfo.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.UserProfileInfo.save()

#####################
class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)

	nickname = models.CharField(max_length=15,default='SOME STRING')

	portfolio_site = models.URLField(blank=True)

	profile_pic = models.ImageField(upload_to='profile_pics',default='profile.jpg')

	def __str__(self):
		return self.user.username



# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.UserProfileInfo.save()