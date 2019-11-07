# # dappx/forms.py

# from django import forms
# from dappx.models import UserProfileInfo
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class UserCreateForm(forms.ModelForm):
# 	password = forms.CharField(widget=forms.PasswordInput())
# 	#user_id = forms.CharField(required=True)
# 	class Meta():
# 		model = User
# 		fields = ('username','password','email')

# # class UserCreateForm(forms.ModelForm):
# # 	class Meta():
# # 		model = User
# # 		fields = ('user_id')

# class UserProfileInfoForm(forms.ModelForm):
#     class Meta():
#          model = UserProfileInfo
#          #fields = ('portfolio_site','profile_pic')
#          fields = ('userid')

from django import forms
from dappx.models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	#confirm_password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
	
	nickname = forms.CharField(max_length=15,required=True)

	class Meta():
		model = UserProfileInfo
		fields = ('nickname',)
        #fields = ('nickname')

class ProfilePicUpdateForm(forms.ModelForm):
	class Meta():
		model = UserProfileInfo
		fields = ['profile_pic',]


class ProfilePwUpdateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	#password1 = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('password',)
