from django import forms
from dappx.models import UserProfileInfo, Transaction
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username','password','email')

class UserProfileInfoForm(forms.ModelForm):
	
	nickname = forms.CharField(max_length=15,required=True)

	class Meta():
		model = UserProfileInfo
		fields = ('nickname',)

class ProfilePicUpdateForm(forms.ModelForm):
	class Meta():
		model = UserProfileInfo
		fields = ['profile_pic',]


class ProfilePwUpdateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = ('password',)


class TransactionsForm(forms.ModelForm):
	transact=forms.CharField(max_length=18,required=False)
	class Meta():
		model = Transaction
		fields = ('Donor','transact')
