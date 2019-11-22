from django.shortcuts import render, redirect
from dappx.forms import UserForm,UserProfileInfoForm,ProfilePwUpdateForm,ProfilePicUpdateForm,TransactionsForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from dappx.models import Transaction, Friends

# Create your views here.

def index(request):
	return render(request,'dappx/index.html')

def usermain(request):
    return render(request,'dappx/usermain.html')

@login_required
def special(request):
	return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def Reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'dappx/usermain.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dappx/Reset.html', {
        'form': form
    })


@login_required
def update_pic(request):
    if request.method == 'POST':
        # form = ProfilePicUpdateForm(data=request.POST,instance=request.user)
        form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.userprofileinfo)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            messages.success(request, 'Your account has been updated')
            return redirect('usermain')
        else:
            print(form.errors)

    else:
        form = ProfilePicUpdateForm(data=request.POST,instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'dappx/update_pic.html', context)



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
				return HttpResponseRedirect(reverse('usermain'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'dappx/login.html', {})


#####################################
def Friendstab(request):
    friendobj = Friends.objects.get_or_create(current_user=request.user)
    friends_of_curr_user = friendobj[0].Friendslist.all()
    return render(request, 'dappx/Friends.html',{'friends':friends_of_curr_user,
                                                    })

#####################################
def Groups(request):
    return render(request, 'dappx/Groups.html')

#####################################

###DONOT DELETE

###
# def Transactions(request):
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.save()
#         else:
#             print(user_form.errors)
#     else:
#         user_form = UserForm()
#     return render(request,'dappx/Transactions.html',
#                           {'false':False})

#######################################

def Transactions(request):
    if request.method == 'POST':
        Groups = request.POST.get('Group') 
        Receiver = request.POST.get('Receiver')
        Receivers = Receiver.split(',')
        Amount = request.POST.get('Amount')
        Description = request.POST.get('Description')
        user = User.objects.get(id=request.user.id)
        ## DONT DELETE ##
        #Receiver1 = User.objects.get(username=Receiver).pk
        #Receiver2= User.objects.get(id=Receiver1) 
        ###for invalid users an repititon
        if len(Receivers) == len(set(Receivers)) :
            for Receiver in Receivers:
                try:
                    Receiverid = User.objects.get(username=Receiver).pk
                except Exception as e:
                    return render(request, 'dappx/Transactions.html',{'NoReceivers': True})
        else:
            return render(request, 'dappx/Transactions.html',{'DupReceivers': True})
            
        Transactions_form = Transaction(Groups=Groups,Donor=user,Receivers=Receivers,Amount=Amount,Description=Description)
        Transactions_form.save()
        return render(request, 'dappx/test.html',{'test_var1':Receivers,
                                                    'test_var2':Transactions_form.Date})
        if Transactions_form.is_valid():

            transactions = transcations_form.save()
            transactions.save()
        else:
            print(Transactions_form.errors)
    else:
        transcations_form = TransactionsForm(data=request.POST)
    return render(request, 'dappx/Transactions.html')

#########     DONT DELETE     ######
# def addfriends(request):
#     if request.method == 'POST':
#         Friends_str = request.POST.get('Friends')
#         Friendslist = Friends_str.split(',')
#         idlist = [User.objects.get(username=Friend).pk for Friend in Friendslist]
#         # return render(request, 'dappx/test.html',{'test_var1':idlist})
#         user = User.objects.get(id=request.user.id)
#         Friends_form = Friends(Friendof=user)
#         Friends_form.save()
#         for idu in idlist:
#             Friends_form.Friendslist.add(User.objects.get(id=idu))
#             pass
#         Friends_form.save()
#         return render(request, 'dappx/test.html',{'test_var1':Friends_form,
#                                                     'test_var2':idlist})

#########33
def addfriends(request):
    if request.method == 'POST':
        Friends_str = request.POST.get('Friendsl')
        Friendslist = Friends_str.split(',')
        idlist = [User.objects.get(username=Friend).pk for Friend in Friendslist]
        # return render(request, 'dappx/test.html',{'test_var1':idlist})
        # user = User.objects.get(id=request.user.id)
        for idu in idlist:
            Friend2 = User.objects.get(id=idu)
            Friends.make_friend(request.user, Friend2)
            Friends.make_friend(Friend2, request.user)
        
        friendobj = Friends.objects.get(current_user=request.user)
        friends_of_curr_user = friendobj.Friendslist.all()
        return render(request, 'dappx/Friends.html',{'friends':friends_of_curr_user,
                                                    })

def change_friends(request,operation,pk):
    friend = User.objects.get(id=pk)
    if operation == 'add':
        Friends.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)

    return render(request, 'dappx/Friends.html')
    
