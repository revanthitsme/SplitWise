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
from dappx.models import Transaction, Friends, ftoftransaction, GroupsModel, notificationsModel
from django.db.models import Avg, Count, Min, Sum
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
def amount_of_each(request, friendslist, not_exists):
    amount_list = []
    owed_list = []
    owed_friend_list = []
    owe_list = []
    owe_friend_list = []
    nothing_friend_list = []
    for friend in friendslist:
        userid = request.user.pk
        friend_username = friend.username
        friendid = friend.pk
        transactions = ftoftransaction.objects.filter(Donor_id = userid,Receiver_id=friendid)
        owed = transactions.aggregate(Sum('Amount'))
        owed = owed["Amount__sum"]
        #owed_list.append(owed)
        transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid)
        owe = transactions1.aggregate(Sum('Amount'))
        owe = owe["Amount__sum"]
        #owe_list.append(owe)
        if owed is not None and owe is not None:
            if owed > owe:
                owed_list.append(owed - owe)
                owed_friend_list.append(friend)
            elif owe > owed:
                owe_list.append(owe - owed)
                owe_friend_list.append(friend)
            else:
                nothing_friend_list.append(friend)
        elif owed is None and owe is not None:
            if owe > 0:
                owe_list.append(owe)
                owe_friend_list.append(friend)
            else:
                nothing_friend_list.append(friend)
        elif owed is not None and owe is None:
            if owed > 0:
                owed_list.append(owed)
                owed_friend_list.append(friend)
            else:
                nothing_friend_list.append(friend)
        else:
            nothing_friend_list.append(friend)

    owed_dict = {} 
    for key in owed_friend_list: 
        for value in owed_list: 
            owed_dict[key] = value 
            owed_list.remove(value) 
            break
    owe_dict = {} 
    for key in owe_friend_list: 
        for value in owe_list: 
            owe_dict[key] = value 
            owe_list.remove(value) 
            break
    friendobj = Friends.objects.get_or_create(current_user=request.user)
    friends_of_curr_user = friendobj[0].Friendslist.all()
    print("length: ",end=' ')
    for i in range(len(owe_list)):
        print(i, end='  ')
    print("")
    return render(request, 'dappx/Friends.html',
                                    {'owed_dict':owed_dict,'owe_dict':owe_dict,'no_exists':not_exists,
                                    'owe_list':owe_list,'owe_friend_list':owe_friend_list,
                                    'owed_list':owed_list,'owed_friend_list':owed_friend_list,
                                    'nothing_friend_list':nothing_friend_list,'friends':friends_of_curr_user})



#####################################
def Friendstab(request):
    friendobj = Friends.objects.get_or_create(current_user=request.user)
    friends_of_curr_user = friendobj[0].Friendslist.all()
    amount_list = amount_of_each(request, friends_of_curr_user, False)
    return amount_of_each(request, friends_of_curr_user, False)
    return render(request, 'dappx/Friends.html',{'friends':friends_of_curr_user,
                                                    })

#####################################
def Groups(request):
    ftoftransactions_debt = ftoftransaction.objects.filter(Donor=request.user)
    all_groups = GroupsModel.objects.filter(Member=request.user,in_group=True)
    group_names = [Group3.Group for Group3 in all_groups]
    #x = GroupsModel.objects.get(Group=group_names[0])
    #return render(request, )
    print(all_groups)
    group_names = set(group_names)
    print(group_names)
    try:
        group_names.remove('')
    except Exception as e:
        pass
    # print(group_names)
    unique_groups = [Group4 for Group4 in all_groups if Group4.Group in group_names]
    print(unique_groups)
    ###### WON'T PRINT AMOUNT IN GROUPS_TAB Separate function to be created #######
    args = {'debt_group_objs':ftoftransactions_debt,'groups':set(unique_groups)}
    return render(request, 'dappx/Groups.html',args)

#####################################

def Transactions(request):
    if request.method == 'POST':
        Groups = request.POST.get('Group') 
        Receiver = request.POST.get('Receiver')
        Receivers = Receiver.split(',')
        Amount = request.POST.get('Amount')
        Description = request.POST.get('Description')
        Tag = request.POST.get('Tag')
        user = User.objects.get(id=request.user.id)

        ## CHECK WHETHER IF GROUP EXISTS ##
        Groups_exi = GroupsModel.objects.filter(Member_id=request.user.pk,in_group=True)
        # Groups_exi = GroupsModel.objects.all()
        Groups_names = [Group1.Group for Group1 in Groups_exi]
        print(Groups_names)
        print(Groups_names)
        if Groups not in Groups_names or Groups is '' :
            return render(request, 'dappx/Groups.html',{'create_group':True})

        ## CHECKING WHETHER GROUP MEMBERS ARE SAME : RECEIVERS AND USER ##
        gp_Members_obj = GroupsModel.objects.filter(Group=Groups,in_group=True)
        gp_Members = [Group2.Member.username for Group2 in gp_Members_obj if Group2.Member != request.user]
        print(gp_Members)
        print(Receivers)
        if set(gp_Members) != set(Receivers):
            return render(request, 'dappx/Transactions.html',{'not_total':True,'gp_Members':gp_Members,'username':request.user.username})

        ## ADDING ## UPDATING Request User to group ##
        amounteach = int(Amount)/(len(Receivers)+1)
        amount_user = int(Amount) - amounteach
        Group_obj1 = GroupsModel.objects.filter(Group=Groups,Member=user,in_group=True)
        Group_obj1 = Group_obj1[0]
        Group_obj1.Amount = Group_obj1.Amount + amount_user
        Group_obj1.Description = Description
        Group_obj1.Tag = Tag
        Group_obj1.save()
        # Group_obj = GroupsModel(Group=Groups,Member=user,Amount=amount_user,Damount=amount_user,Description=Description,Tag=Tag)
        # Group_obj.save() ## IMPORTANT

        ## DONT DELETE ##
        #Receiver1 = User.objects.get(username=Receiver).pk
        #Receiver2= User.objects.get(id=Receiver1)

        ###for invalid users and repititon
        if len(Receivers) == len(set(Receivers)) :
            for Receiver in Receivers:
                try:
                    Receiverid = User.objects.get(username=Receiver).pk
                except Exception as e:
                    return render(request, 'dappx/Transactions.html',{'NoReceivers': True})
        else:
            return render(request, 'dappx/Transactions.html',{'DupReceivers': True})

        for Receiver1 in Receivers:
            new_friend = User.objects.get(id=User.objects.get(username=Receiver1).pk)
            Friends.make_friend(request.user, new_friend)
            Friends.make_friend(new_friend, request.user)
            
            #Assumption: FtoFTransactions is valid
            if int(Amount)>=0:
                ftoftransaction_form = ftoftransaction(Donor=user,Receiver=new_friend,Amount=amounteach,Damount=amounteach,Description=Description,Group=Groups,Tag=Tag)
            else:
                ftoftransaction_form = ftoftransaction(Donor=new_friend,Receiver=user,Amount=abs(amounteach),Damount=abs(amounteach),Description=Description,Group=Groups,Tag=Tag)
            #ftoftransaction_form = ftoftransaction(Donor=user,Receiver=new_friend,Amount=amounteach,Damount=amounteach,Description=Description,Group=Groups)
            ftoftransaction_form.save()
            #### ADDING TO Groups Model
            negamounteach = -1 * amounteach
            print(negamounteach)
            Group_obj2 = GroupsModel.objects.filter(Group=Groups,Member=new_friend,in_group=True)
            Group_obj2 = Group_obj2[0]
            Group_obj2.Amount = Group_obj2.Amount + negamounteach
            print(Group_obj2.Amount)
            Group_obj2.Description = Description
            Group_obj2.Tag = Tag
            Group_obj2.save()
            # Group_obj = GroupsModel(Group=Groups,Member=new_friend,Amount=negamounteach,Damount=negamounteach,Description=Description,Tag=Tag)
            # Group_obj.save()

        Transactions_form = Transaction(Groups=Groups,Donor=user,Receivers=Receivers,Amount=Amount,Description=Description,Tag=Tag)
        Transactions_form.save()
        ## ACTIVITY OF TRANSACTIONS USE TRANSACTIONS ##
        return render(request, 'dappx/usermain.html')
        if Transactions_form.is_valid():

            transactions = transcations_form.save()
            transactions.save()
        else:
            print(Transactions_form.errors)
    else:
        transcations_form = TransactionsForm(data=request.POST)
    return render(request, 'dappx/Transactions.html')


def addfriends(request):
    if request.method == 'POST':
        Friends_str = request.POST.get('Friendsl')
        Friendslist = Friends_str.split(',')
        try:
            idlist = [User.objects.get(username=Friend).pk for Friend in Friendslist]    
        except Exception as e:
            friendobj = Friends.objects.get_or_create(current_user=request.user)
            friends_of_curr_user = friendobj[0].Friendslist.all()
            amount_list = amount_of_each(request, friends_of_curr_user, True)
            return amount_of_each(request, friends_of_curr_user, True)

        for idu in idlist:
            Friend2 = User.objects.get(id=idu)
            Friends.make_friend(request.user, Friend2)
            Friends.make_friend(Friend2, request.user)
        ## DONT DELETE ##
        #friendobj = Friends.objects.get(current_user=request.user)
        #friends_of_curr_user = friendobj.Friendslist.all()
    return Friendstab(request)

# def change_friends(request,operation,pk):
#     friend = User.objects.get(id=pk)
#     if operation == 'add':
#         Friends.make_friend(request.user, friend)
#     elif operation == 'remove':
#         Friend.lose_friend(request.user, friend)

#     return render(request, 'dappx/Friends.html')

#######
def view_friend(request, pk):
    Friend2 = User.objects.get(id=pk)
    friend_username = Friend2.username
    friendid = pk
    userid = request.user.pk
    username = request.user.username

    ##friend owes how much
    transactions = ftoftransaction.objects.filter(Donor_id = userid,Receiver_id=friendid)
    
    ##how much does user owe to friend
    transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid)
    for transaction1 in transactions:
        print(transaction1)
    ## ONLY DIFFERENT GROUPS BY SUMMING THE AMOUNTS ##
    ######
    ## UPDATING  ##
    return render(request, 'dappx/view_friend.html',{'transactions1':transactions1, 'transactions':transactions, 'friend':Friend2})

#######
def view_group(request, operation):
    print(type(operation)) ## operation is group name ##
    #print(operation.Amount)
    Member_objs = GroupsModel.objects.filter(Group=operation,in_group=True)
    print(Member_objs)
    print('view_group')
    Mem_Am_dict = {}
    for obj in Member_objs:
        Mem_Am_dict[obj.Member] = obj.Amount
    print(Mem_Am_dict)
    Mem_Am_dict.pop(request.user, None)
    ### SETTLING IN GROUPS MODEL ###

    return render(request, 'dappx/view_group.html',{'members_dict':Mem_Am_dict,'group':operation})
##########
def Leave_group(request, operation1):
    #print(operation1.Amount)
    Member_objs = GroupsModel.objects.filter(Group=operation1)
    group_obj2 = GroupsModel.objects.filter(Group=operation1,Member=request.user)
    group_obj2 = group_obj2[0]
    print(Member_objs)
    print(type(group_obj2.Amount))
    print("dfghjklknb")
    #print(operation)
    #print(type(operation))
    #print(request.user)
    Amount1 = group_obj2.Amount
    print(Amount1)
    print(type(Amount1))
    print(Amount1 == 0)
    if Amount1 != 0:
        ftoftransactions_debt = ftoftransaction.objects.filter(Donor=request.user)
        all_groups = GroupsModel.objects.filter(Member=request.user,in_group=True)
        group_names = [Group3.Group for Group3 in all_groups]
        group_names = set(group_names)
        try:
            group_names.remove('')
        except Exception as e:
            pass
        unique_groups = [Group4 for Group4 in all_groups if Group4.Group in group_names]
        args = {'debt_group_objs':ftoftransactions_debt,'groups':set(unique_groups),'cannot_settle':True}
        return render(request, 'dappx/Groups.html',args)
    else:
        print(group_obj2.Member)
        print(group_obj2.Amount)
        group_obj2.in_group = False
        group_obj2.save()
        ftoftransactions_debt = ftoftransaction.objects.filter(Donor=request.user)
        all_groups = GroupsModel.objects.filter(Member=request.user,in_group=True)
        group_names = [Group3.Group for Group3 in all_groups]
        group_names = set(group_names)
        try:
            group_names.remove('')
        except Exception as e:
            pass
        unique_groups = [Group4 for Group4 in all_groups if Group4.Group in group_names]
        args = {'debt_group_objs':ftoftransactions_debt,'groups':set(unique_groups),'cannot_settle':False}
    return render(request, 'dappx/Groups.html',args)

##########
def settle_up(request, pk):
    Friend3 = User.objects.get(id=pk)
    friend_username = Friend3.username
    friendid = pk
    userid = request.user.pk
    username = request.user.username
    ##friend owes how much
    #transactions = ftoftransaction.objects.filter(Donor_id = userid,Receiver_id=friendid).update(Amount=0)
    transactions = ftoftransaction.objects.filter(Donor_id = userid,Receiver_id=friendid)
    for transaction in transactions:
        #write code here
        cGroup = transaction.Group
        amount1 = transaction.Amount
        cGroup_obj_user = GroupsModel.objects.filter(Member=request.user,Group=cGroup)
        cGroup_obj_fr = GroupsModel.objects.filter(Member=Friend3,Group=cGroup)
        cGroup_obj_user = cGroup_obj_user[0]
        cGroup_obj_fr = cGroup_obj_fr[0]
        cGroup_obj_user.Amount = cGroup_obj_user.Amount - amount1
        cGroup_obj_user.save()
        cGroup_obj_fr.Amount = cGroup_obj_fr.Amount + amount1
        cGroup_obj_fr.save()
        transaction.Amount = 0
        transaction.save()
    ##how much does user owe to friend
    #transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid).update(Amount=0)
    transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid)
    for transaction in transactions1:
        #and here
        cGroup = transaction.Group
        amount1 = transaction.Amount
        cGroup_obj_user = GroupsModel.objects.filter(Member=Friend3,Group=cGroup)
        cGroup_obj_fr = GroupsModel.objects.filter(Member=request.user,Group=cGroup)
        cGroup_obj_user = cGroup_obj_user[0]
        cGroup_obj_fr = cGroup_obj_fr[0]
        cGroup_obj_user.Amount = cGroup_obj_user.Amount - amount1
        cGroup_obj_user.save()
        cGroup_obj_fr.Amount = cGroup_obj_fr.Amount + amount1
        cGroup_obj_fr.save()
        transaction.Amount = 0
        transaction.save()
     ## UPDATING  ##
    return render(request, 'dappx/view_friend.html',{'transactions1':transactions1, 'transactions':transactions, 'friend':Friend3})

def creategroup(request):
    if request.method == 'POST':
        Friends_str = request.POST.get('gfriends')
        Group_str = request.POST.get('group_name')
        Friendslist = Friends_str.split(',')
        user = request.user
        # groups_obj_all = GroupsModel.objects.filter(Member_id=user.pk)
        groups_obj_all = GroupsModel.objects.all()
        for groups_obj in groups_obj_all:
            if Group_str == groups_obj.Group:
                print("Already Exists")
                return render(request, 'dappx/Groups.html',{'Exists': True})

        ## ADDING Request User to group
        Group_obj = GroupsModel(Group=Group_str,Member=user,Amount=0,Damount=0,Description="created a new Group",Tag="creation")
        Group_obj.save() ## IMPORTANT

        ###for invalid users and repititon
        if len(Friendslist) == len(set(Friendslist)) :
            for Friend4 in Friendslist:
                try:
                    new_friend = User.objects.get(username=Friend4)
                    Friend4id = new_friend.pk
                    #### ADDING TO FToFTransactions ####
                    transaction0 = ftoftransaction(Donor=user,Receiver=new_friend,Amount=0,Damount=0,Description="created a new Group",Group=Group_str,Tag="creation")
                    transaction0.save()
                    #### ADDING TO Groups Model
                    Group_obj = GroupsModel(Group=Group_str,Member=new_friend,Amount=0,Damount=0,Description="created a new Group",Tag="creation")
                    Group_obj.save()
                    ## IF wanted add to transaction table too.
                    #########
                except Exception as e:
                    return render(request, 'dappx/Groups.html',{'NoFriend': True})
        else:
            return render(request, 'dappx/Groups.html',{'DupFriends': True})

        idlist = [User.objects.get(username=Friend).pk for Friend in Friendslist]
        for idu in idlist:
            Friend2 = User.objects.get(id=idu)
            Friends.make_friend(request.user, Friend2)
            Friends.make_friend(Friend2, request.user)
    return Groups(request)

def notifications(request):
    user = request.user
    messages_objects = notificationsModel.objects.filter(Receiver=user)
    messages_objects_unseen = notificationsModel.objects.filter(Receiver=user,seen=0)
    messages_objects_seen = notificationsModel.objects.filter(Receiver=user,seen=1)
    x = len(messages_objects_unseen)
    for messobj in messages_objects_unseen:
        print(messobj.seen)
    for messobj in messages_objects_seen:
        print(messobj.seen)

    for messobj in messages_objects:
        #messages.append(messobj.message)
        messobj.seen = 1
        messobj.save()
    for messobj in messages_objects:
        print(messobj.seen)
    return render(request, 'dappx/notifications.html',{'unotifications_seen':messages_objects_seen,'unotifications_unseen':messages_objects_unseen})

def send_notification(request,pk):
    if request.method == 'POST':
        message = request.POST.get('Message')
        friend = User.objects.get(id=pk)
        #print(message)
        #if message is "":
        #    print("None")
        if(message is ""):
            return render(request,'dappx/send_notification.html',{'no_message':True,'friend':friend})
        else:
            notification_object = notificationsModel(Sender=request.user,Receiver=friend,message=message,seen=0)
            notification_object.save()
            return redirect('usermain')

    else:
        friend = User.objects.get(id=pk)
        return render(request,'dappx/send_notification.html',{'friend':friend})