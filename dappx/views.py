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
from dappx.models import Transaction, Friends, ftoftransaction, notificationsModel
from django.db.models import Avg, Count, Min, Sum
import json
from django.core import serializers
import csv
import pandas as pd
# Create your views here.
#notifications_num = 0
def index(request):
	return render(request,'dappx/index.html')

def usermain(request):
    user = request.user
    # messages_objects_unseen = notificationsModel.objects.filter(Receiver=user,seen=0)
    # x = len(messages_objects_unseen)
    # notifications_num = x
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


@login_required
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
@login_required
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
@login_required
def amount_of_each(request, friendslist):
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
    return render(request, 'dappx/Friends.html',{'owed_dict':owed_dict,'owe_dict':owe_dict,'owe_list':owe_list,'owe_friend_list':owe_friend_list,
            'owed_list':owed_list,'owed_friend_list':owed_friend_list,'nothing_friend_list':nothing_friend_list,'friends':friends_of_curr_user})



#####################################
@login_required
def Friendstab(request):
    friendobj = Friends.objects.get_or_create(current_user=request.user)
    friends_of_curr_user = friendobj[0].Friendslist.all()
    amount_list = amount_of_each(request, friends_of_curr_user)
    return amount_of_each(request, friends_of_curr_user)
    return render(request, 'dappx/Friends.html',{'friends':friends_of_curr_user,
                                                    })

#####################################
@login_required
def Groups(request):
    return render(request, 'dappx/Groups.html')

#####################################
@login_required
def Transactions(request):
    if request.method == 'POST':
        Groups = request.POST.get('Group') 
        Receiver = request.POST.get('Receiver')
        Receivers = Receiver.split(',')
        Amount = request.POST.get('Amount')
        Description = request.POST.get('Description')
        Tag = request.POST.get('Tag')
        user = User.objects.get(id=request.user.id)
        ## DONT DELETE ##
        #Receiver1 = User.objects.get(username=Receiver).pk
        #Receiver2= User.objects.get(id=Receiver1) 
        ###for invalid users and repititon
        ##creating only Tags as shown movies, food, housing, travel, others
        Tags_approved = ["Movies","Food","Housing","Travel","Others"]
        if len(Receivers) == len(set(Receivers)) :
            for Receiver in Receivers:
                try:
                    Receiverid = User.objects.get(username=Receiver).pk
                except Exception as e:
                    return render(request, 'dappx/Transactions.html',{'NoReceivers': True})
        else:
            return render(request, 'dappx/Transactions.html',{'DupReceivers': True})

        if Tag in Tags_approved:
            for Receiver1 in Receivers:
                new_friend = User.objects.get(id=User.objects.get(username=Receiver1).pk)
                Friends.make_friend(request.user, new_friend)
                Friends.make_friend(new_friend, request.user)
                amounteach = int(Amount)/(len(Receivers)+1)
                #Assumption: FtoFTransactions is valid
                if int(Amount)>=0:
                    ftoftransaction_form = ftoftransaction(Donor=user,Receiver=new_friend,Amount=amounteach,Damount=amounteach,Description=Description,Group=Groups)
                    pass
                else:
                    ftoftransaction_form = ftoftransaction(Donor=new_friend,Receiver=user,Amount=abs(amounteach),Damount=abs(amounteach),Description=Description,Group=Groups)
                #ftoftransaction_form = ftoftransaction(Donor=user,Receiver=new_friend,Amount=amounteach,Damount=amounteach,Description=Description,Group=Groups)
                ftoftransaction_form.save()

            Transactions_form = Transaction(Groups=Groups,Donor=user,Receivers=Receivers,Amount=Amount,Description=Description,Expenditure=abs(amounteach))
            Transactions_form.save()
            return redirect('usermain')
            if Transactions_form.is_valid():

                transactions = transcations_form.save()
                transactions.save()
            else:
                print(Transactions_form.errors)
        else:
            return render(request,'dappx/Transactions.html',{'Tag_not_approved': True})
                
    else:
        transcations_form = TransactionsForm(data=request.POST)
        return render(request, 'dappx/Transactions.html')

@login_required
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
    return Friendstab(request)

# def change_friends(request,operation,pk):
#     friend = User.objects.get(id=pk)
#     if operation == 'add':
#         Friends.make_friend(request.user, friend)
#     elif operation == 'remove':
#         Friend.lose_friend(request.user, friend)

#     return render(request, 'dappx/Friends.html')
@login_required    
def view_friend(request, pk):
    Friend2 = User.objects.get(id=pk)
    friend_username = Friend2.username
    friendid = pk
    userid = request.user.pk
    username = request.user.username

    ##friend owes how much
    transactions = ftoftransaction.objects.filter(Donor_id = userid,Receiver_id=friendid)
    #transactions = Transaction.objects.all()
    ####
    ##how much does user owe to friend
    transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid)
    for transaction1 in transactions:
        print(transaction1)

    return render(request, 'dappx/view_friend.html',{'transactions1':transactions1, 'transactions':transactions, 'friend':Friend2})

@login_required
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
        transaction.Amount = 0
        transaction.save()
    ##how much does user owe to friend
    #transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid).update(Amount=0)
    transactions1 = ftoftransaction.objects.filter(Donor_id = friendid,Receiver_id=userid)
    for transaction in transactions1:
        transaction.Amount = 0
        transaction.save()
    return render(request, 'dappx/view_friend.html',{'transactions1':transactions1, 'transactions':transactions, 'friend':Friend3})

@login_required
def creategroup(request):
    return render(request, 'dappx/Groups.html')

@login_required
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


@login_required
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

@login_required
def time_series_plots(request):
    return render(request,'dappx/time_series_plots.html')



@login_required
def tagplots(request):
    if request.method == 'POST':
        fromdate = request.POST.get('From')
        todate = request.POST.get('To')
        # Tag = request.POST.get('Tag')
        if(fromdate=="" or todate==""):
            return render(request,'dappx/time_series_plots.html',{'not_entered':True})
        print(fromdate)
        user = request.user
        Tags_approved = ["Movies","Food","Housing","Travel","Others"]
        #########################
        #for time line series
        Tag_approved_lists = {}
        dates_approved_objects2 = Transaction.objects.filter(Date2__gte=fromdate,Date2__lte=todate)
        dates_approved_objects = []
        for i in dates_approved_objects2:
            group_members = i.Receivers
            group_members.append(i.Donor.username)
            if user.username in group_members:
                dates_approved_objects.append(i)
        dates_approved = []
        for i in dates_approved_objects:    
            if i.Date2 in dates_approved:
                print("happy")
            else:
                dates_approved.append(i.Date2)
        for i in Tags_approved:
            money_per_tag_per_date = []
            for j in dates_approved:
                money=0
                for k in dates_approved_objects:
                    if(k.Date2==j and k.Tag==i):
                        money = money + k.Expenditure
                money_per_tag_per_date.append(money)

            Tag_approved_lists[i]=money_per_tag_per_date   

        ##############################
        #data approved objects
        fields = ['Groups','Donor','Receivers','Description','Amount','Tag','Date','Date2','Expenditure']
        rows =[]
        for i in dates_approved_objects:
            row1 = [i.Groups,i.Donor,i.Receivers,i.Description,i.Amount,i.Tag,i.Date,i.Date2,i.Expenditure]
            rows.append(row1)
            

        with open('exceelsheet.csv', 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
          
        # writing the fields 
        #   csvwriter.writerow(fields) 
          
        # writing the data rows 
            csvwriter.writerows(rows)
            #csvwriter.columns(fields)
        print(rows)
        htmlwriter = pd.read_csv('exceelsheet.csv',names=fields)
        html_str=htmlwriter.to_html()
        # html_file=open('../templates/dappx/plot.html','a')
        # html_file.write(html_str)
        # html_file.close()
            ####################################
            # money_per_tag_per_date = []
            # for i in dates_approved:
            #     money =0
            #     for j in dates_approved_objects:
            #         if (j.Date2==i):
            #             money = money + j.Expenditure
            #     money_per_tag_per_date.append(money)

            
        #for piechart1 (tags,expenditure)
        
        Tags_values=[]
        for Tag1 in Tags_approved:
            

            objectfortags = Transaction.objects.filter(Tag=Tag1,Date2__gte=fromdate,Date2__lte=todate)
            
            money_spent =0

            for obj in objectfortags:
                group_members = objectfortags.Receivers
                group_members.append(objectfortags.Donor.username)
                if user.username in group_members:
                    money_spent = money_spent + obj.Expenditure
                    Tags_values.append(money_spent)
        ###########
        #for time line series
        # dates_objects = Transaction.
        ############
        #for piechart2 (friends,expenditure)
        friends_objects1 = ftoftransaction.objects.filter(Donor=request.user,Date2__gte=fromdate,Date2__lte=todate)
        friends_objects2 = ftoftransaction.objects.filter(Receiver=request.user,Date2__gte=fromdate,Date2__lte=todate)
        friends_names=list()
        friends_usernames =[]
        for i in friends_objects1:
            if i.Receiver in friends_names:
                print("happy")
            else:
                friends_names.append(i.Receiver)
                friends_usernames.append(i.Receiver.username)
        for i in friends_objects2:
            if i.Donor in friends_names:
                print("happy")
            else:
                friends_names.append(i.Donor) 
                friends_usernames.append(i.Receiver.username)  
        money_value_for_friend=list()
        money_given_by_me = []
        money_given_by_frnd=[]
        for i in friends_names:
            money = 0
            money1=0
            money2=0
            for j in friends_objects1:
                if(j.Receiver==i):
                    money = money + j.Damount
                    money1 = money1 + j.Damount
            for j in friends_objects2:
                if(j.Donor==i):
                    money = money + j.Damount
                    money2 = money2 + j.Damount
            money_value_for_friend.append(money)
            money_given_by_frnd.append(money2)
            money_given_by_me.append(money1)
        for i in friends_names:
            print(i)
        for i in money_value_for_friend:
            print(i)
        ############
        # groups that frnd is in
        group_names=[]
        for i in friends_objects1:
            if i.Group in group_names:
                print('happy')
            else:
                group_names.append(i.Group)
        for i in friends_objects2:
            if i.Group in group_names:
                print('happy')
            else:
                group_names.append(i.Group)
        money_given_to_group=[]
        money_given_to_me_by_group=[]
        for i in group_names:
            money1=0
            money2=0
            for j in friends_objects1:
                if(j.Group==i):
                    money1=money1+j.Damount
            for j in friends_objects2:
                if(j.Group==i):
                    money2=money2+j.Damount
            money_given_to_group.append(money1)
            money_given_to_me_by_group.append(money2)


        ########### 
        #for stacked  bargraph1 
        # group_objects = ftoftransaction.objects.filter() 
        #for piechart1 (tags,expenditure)  
        chart1 = {
            'chart':{'type':'pie'},
            'title':{'text':'pie chart for expenditure with tags'},
            'series': [{
                'name':'Total Transaction Amount',
                'data':list(map(lambda row1,row2:{'name':row1,'y': row2},Tags_approved,Tags_values))
            }]
        }
        ##########
        ############
        #for piechart2 (friends,expenditure)
        chart2 = {
            'chart':{'type':'pie'},
            'title':{'text':'pie chart for expenditure with friends'},
            'series':[{
                'name':'Total Amount',
                'data':list(map(lambda row1,row2:{'name':row1,'y':row2},friends_usernames,money_value_for_friend))
            }]
        }
        ################
        #for chart3(frnd,owed,owe)
        lent_series = {
            'name':'lent',
            'data':money_given_by_me,
            'color':'blue',
        }
        borr_series = {
            'name':'borrowed',
            'data':money_given_by_frnd,
            'color':'red',
        }

        chart3 = {
            'chart':{'type':'bar'},
            'plotOptions' :{
                'series':{
                    'stacking':'normal'
                }
            },
            'title':{'text':'Bar Graph For Friends'},
            'xAxis':{'categories':friends_usernames},
            'series':[lent_series,borr_series]
        }
        ##############
        #for chart4(group,owed,owe)
        group_lent_series = {
            'name':'lent',
            'data':money_given_to_group,
            'color':'blue',
        }
        group_borr_series = {
            'name':'borrowed',
            'data':money_given_to_me_by_group,
            'color':'red',
        }

        chart4 = {
            'chart':{'type':'bar'},
            'plotOptions' :{
                'series':{
                    'stacking':'normal'
                }
            },
            'title':{'text':'Bar Graph For Groups'},
            'xAxis':{'categories':group_names},
            'series':[group_lent_series,group_borr_series]
        }
        #################
        #chart5 (tag,expenditure)
        #"Movies","Food","Housing","Travel","Others"
        chart5 = {
            'chart':{'type':'area'},
            'title':{'text':'Time Series Plot for expenditure for different tags'},
            'xAxis':{
                'categories':dates_approved
            },
            'series':[{
                'name':'Money Spent on Movies',
                'data':Tag_approved_lists["Movies"]
            },{
                'name':'Money spent on Food',
                'data':Tag_approved_lists["Food"]
            },{
                'name':'Money spent on Housing',
                'data':Tag_approved_lists["Housing"]
            },{
                'name':'Money spent on Travel',
                'data':Tag_approved_lists["Travel"]
            },{
                'name':'Money spent on Others',
                'data':Tag_approved_lists["Others"]
            }]
        }
        #############
        dump1 = json.dumps(chart1)
        dump2 = json.dumps(chart2)
        dump3 = json.dumps(chart3)
        dump4 = json.dumps(chart4)
        dump5 = json.dumps(chart5)
        ##############


        return render(request,'dappx/plot.html',{'chart1':dump1,'chart2':dump2,'chart3':dump3,'chart4':dump4,'chart5':dump5,'excel':html_str})
    else:
        return render(request,'dappx/time_series_plots.html')

