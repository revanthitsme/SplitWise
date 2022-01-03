Splitwise

The following description only plots little dots. You need to connect the dots by making conscious choices during your implementation. There will be points for the reason behind every choice made. Naturally, how well you connect the dots will determine how good the whole picture looks.


The project is to implement a clone of the popular web and mobile application Splitwise. Splitwise makes it easy to split bills with friends and family. It organizes all your shared expenses in one place, so that everyone can see who they owe. Whether you are sharing a ski vacation, splitting rent with roommates, or paying someone back for lunch, Splitwise makes life easier.



A. Basic Features


User Authentication

Create a registration system so that a new user can register with his name, userid (nickname), password and recovery mail (optional). Later he can login with his username and password. Its upto you to add a forgot password and send a random token to the mail (optional). Once he logins he must have an option to change his password and not his userid. Once the user logs in he can add extra info

I.e., personal details (optional) but there must be an option to add display picture to his profile, which must be displayed on the dashboard. (compulsory).


Dashboard Creation
The main design core of the splitwise app is the frontend dashboard pattern. So the main things you need to have in the dashboard.


Friends tab
 A list of all your friends with the amount of money you owe or he/she owes to you.
Option to add friends to your friends circle.
On clicking any friend in the list, a detailed list of how much you owe or he/she owe to you in every group should be displayed with a “Settle Up” option at the top..
Now there are two things.

From this list you should be able to click on any group and then the corresponding group page (similar to if you open from group tab) should be displayed.
On clicking “Settle Up” option, automatically created “settle up” transactions should appear in all groups where you owe or he/she owes to you to nullify.
I.e., You and this friend are all settled up in all groups !!


Groups tab
A list of all your groups with the net amount of money you owe or the group owes to you.
Option to create new groups by adding friends from your friend circle.
Option to leave or delete a  group, note you must be able to do only if you are
settled up.

IV.        On clicking any group in the list, a detailed list of all transactions in the

group  should be displayed with two buttons at the top “Settle Up” and “Balances” , where

Balances - At the top, how much everyone owes or you need to give and below net amount any other owes/ gets from the group.
Settle Up - This should give the option to settle up with whom in the group and you need to able to pick multiple friends and this should automatically create  “settled up” transactions in the group. (No interference with other groups)

Activity tab
I.   Lists all the activity related to you happening in various groups in this tab.

II. The activity must include you owe/ someone owes, comments, tag changes or name changes as well.

 

Transactions
The design of transactions is another novel concept which we will change a little to make it spicy !!


 Every transaction must include options for the following :

Which group the transaction belongs to.
Who are the stakeholders of the transaction.
Enter description and amount involved in the transaction.
Splitting of the money among the stakeholders (have option to split equally (automatic) and unequally (option to specify))
Tag the transaction (to some predefined categories like movies, food, housing, travel, others.)

In the backend you need to also log the time and date of this transaction also.


Insights

This is an option available in Splitwise Pro, you will need to create the following things in the insights tab.


Take a date range from the user and create an excel sheet with all transactions.
(This excel sheet should contain all the info to plot the graphs below)

Plot some ‘really’ interesting plots
time series plot of expenditure spent on food, housing, etc
pie chart showing
expenditure spent over food, housing, movies, etc.
expenditure exchanged (given or taken) over friends.
bar chart showing
net amount owing and lent as a stacked bar chart  vs the groups.
net amount owing and lent as a stacked bar chart  vs friends
Any innovative chart different from above three which gives more insight.
Option to print a report containing the plots and the transaction history in a proper pdf.
                 (The pdf should be properly legible and easily understandable)


Additional Features (Suggestions) [Min required = 1 ]

Minimise the number of transactions within each group. (Simplify group debts feature). For example, suppose A, B and C are in a group. Suppose A lends B $30 and B lends C $20 and C lends A $40., instead of  (a) it should give (b)
B owes $30 to A, C owes $20 to B, A owes $40 to C
B owes $10 to A, A owes $20 to C
        (This need not be perfectly optimistic, any heuristic which reduces transactions significantly

        should work)

Remind option wherever there is  “Settle Up” to remind your friend to give the money he/she owes it to you. This should send a notification with the message you entered while clicking remind option to him. (It’s up to you how you send this notification, either you have a notification icon receiving the message or  a push notification)
Add a camera or upload photo option whenever you are adding a transaction so that you can add multiple bills and it will calculate the net amount and also autosuggest the tag and description for you. Figure out the OCR libraries and discuss with the TA’s

You can also come up with your own additional features but you need to get the approval from the TA’s assigned to the project.


Note
I tried to be as clear as possible, but If you find some point to be confusing just open the splitwise app and look how it is there and go ahead. Incase you still have a doubt contact the TA’s assigned.
You need to design your own schema and keep the database tables as simple as possible.
It is up to you whether you make an Android Application or Web Application. Make sure that all the features are implemented on the same chosen platform.

Good Tools and Frameworks:

You can use Django as backend for both Android and web interface
For web interface, you can use HTML, CSS, JS, jQuery for frontend
For android app, you can use Android Studio
You can use the default database that comes with Django. (Use Firebase at your own risk)
