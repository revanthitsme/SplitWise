from django.shortcuts import render, redirect
#from dappx.forms import UserCreateForm #,UserProfileInfoForm
from dappx.forms import UserForm,UserProfileInfoForm,ProfilePwUpdateForm,ProfilePicUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.

def index(request):
	return render(request,'dappx/index.html')

@login_required
def special(request):
	return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

# def Reset(request):
# 	if request.method == 'POST':
# 		newpassword = request.POST.get('new_password')
# 		newpassword1 = request.POST.get('new_password1')
# 		if (newpassword == newpassword1):
# 			#old = request.user.username
# 			#old = request.user.password
# 			request.user.set_password(newpassword) 
# 			request.user.password = newpassword
# 			old = request.user.password
# 			request.user.save()
# 			#user.set_password(newpassword)
# 			return render(request,'dappx/test.html',{'test_var':old})
# 		else:
# 			print("both passwords are different")
# 			return render(request, 'dappx/Reset.html', {'wrong':True})

# 	else:
# 		return render(request, 'dappx/Reset.html', {})

def Reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            #return redirect('change_password')
            return render(request, 'dappx/base.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dappx/Reset.html', {
        'form': form
    })


@login_required
def update(request):
    if request.method == 'POST':
        form = ProfilePicUpdateForm(data=request.POST,instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            messages.success(request, 'Your account has been updated')
            return redirect('base')
        else:
            print(form.errors)

    else:
        form = ProfilePicUpdateForm(data=request.POST,instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'dappx/update.html', context)


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('login:change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     response = render(request, 'password_change.html', {
#         'form': form
#     })
#     response.set_cookie('password_changed', 'true')
#     return response 

	
# def Reset(request):
# 	if request.method == 'POST':
# 		pw_up_form = ProfilePwUpdateForm(data=request.POST,instance=request.user)
# 		if pw_up_form.is_valid():
# 			pw_rst = pw_up_form.save()
# 			old = request.user.password
# 			pw_rst.save()
# 			new = request.user.password

# 			return render(request,'dappx/test.html',{'test_var1':old,'test_var2':new,})
# 		else:
# 			print(pw_up_form.errors)
# 	else:
# 		pw_up_form = ProfilePwUpdateForm(data=request.POST)
# 		return render(request,'dappx/Reset.html', {'reset_form':pw_up_form,
# 												})



# def register(request):
# 	registered = False
# 	#user.is_authenticated = False
# 	if request.method == 'POST':
# 		#UserCreateForm.objects.create(user_id='test')
# 		user_form = UserCreateForm(data=request.POST)

# 		profile_form = UserProfileInfoForm(data=request.POST)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			user = user_form.save()
# 			user.set_password(user.password)
# 			#create_user_profile(user, 'userid', True)
# 			#userid.user = user.user_id
# 			#userid = user_id
# 			#print(user.userid)
# 			user.save()
# 			profile = profile_form.save(commit=False)
# 			profile.user = user
# 			#if 'profile_pic' in request.FILES:
# 			#	print('found it')
# 			#	profile.profile_pic = request.FILES['profile_pic']
# 			#profile.save()
# 			registered = True
# 		else:
# 			print(user_form.errors,profile_form.errors)
# 	else:
# 		user_form = UserCreateForm()
# 		#profile_form = UserProfileInfoForm()
# 	return render(request,'dappx/registration.html',
#                           {'user_form':user_form,
#                           	#'auth':user.is_authenticated,
#                            #'profile_form':profile_form,
#                            'registered':registered})

###########

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #nickname = user_form.nickname
            #return render(request, 'dappx/test.html',{'test_var':nickname})
            user.set_password(user.password)
            #user.first_name = nickname
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # if 'profile_pic' in request.FILES:
            #     print('found it')
            #     profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'dappx/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

###########
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'dappx/login.html', {})


