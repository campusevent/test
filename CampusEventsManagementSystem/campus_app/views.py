from django.shortcuts import render, redirect
from campus_app.forms import UserForm  
from campus_app.models import User, Event, Account, Registration, Feedback
from django.contrib import messages
from campus_app.functions import handle_uploaded_file
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal


import random as rd
# Create your views here.

def index(request):
     return render(request, "homepages/index.html", {})

def login(request):
     return render(request, "homepages/login.html", {})

def validate_user_login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get("email"))
            print('userId=', user.userId)
            print('userType=', user.userType)
            print("password===" , user.password)
            if user.password == request.POST.get("password") and user.userType == request.POST.get("userType") :
                request.session['userId'] = user.userId
                request.session['userName'] = user.firstName + ' ' +user.lastName
                request.session['userType'] = user.userType
                
                if user.userType == "Organizer":
                    return render(request,'organizer/home.html', {'user':user})
                elif user.userType == "Attendee":
                    return render(request,'attendee/home.html', {'user':user})

            else:
                messages.error(request, "Invalid User.")
                return redirect("/login")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("/login")
        except Exception as e1:
            messages.error(request, "Invalid User1.")
            print("error: ", str(e1))
            return redirect("/login")



def user_registration(request): 
    return render(request,'homepages/user_registration.html',{})  
     

def add_user_registration(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password") 
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        mobile = str(request.POST.get("mobile"))
        course = request.POST.get("course")
        
        userPic = str(rd.randint(1, 10000)) + request.FILES['userPic'].name
        userType = request.POST.get("userType")
        handle_uploaded_file(request.FILES['userPic'], userPic) 


        if password != confirm_password:
            messages.error(request, "Passwords not match.")
            return redirect("user_registration")

        
        user = User.objects.create(
            firstName=firstName,
            lastName=lastName,
            email=email,
            mobile=mobile,
            course=course,
            userPic=userPic,
            userType=userType,
            password = password
        )
        user.save()
        return redirect("/login")


    return redirect("user_registration")


def logout(request):
    return render(request, "homepages/index.html", {})

def home(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request,'organizer/home.html', {"user": user})

def attendee_home(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request,'attendee/home.html', {"user": user})

def profile(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "organizer/profile.html", {"user": user})


def update_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        mobile = str(request.POST.get("mobile"))
        course = request.POST.get("course")
        userType = request.POST.get("userType")

        
        user = User.objects.get(email=email)
        user.firstName=firstName
        user.lastName=lastName
        user.email=email
        user.mobile=mobile
        user.course=course
        user.userType=userType
        user.password = password
        
        user.save()
       


    return redirect("/profile")


def add_event_form(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "organizer/add_event.html", {"user": user})



def add_event_code(request):
    try:
        if request.method == "POST":
            userId = request.session['userId']
            eventType = request.POST.get("eventType")
            eventTitle = request.POST.get("eventTitle") 
            description = request.POST.get("description")
            eventposter = str(rd.randint(1, 10000)) + request.FILES['eventposter'].name
            handle_uploaded_file(request.FILES['eventposter'], eventposter) 
            eventDateTime = str(request.POST.get("eventDateTime"))
            eventLocation = request.POST.get("eventLocation")
            eventFee = request.POST.get("eventFee")
            totalAttendees = request.POST.get("totalAttendees")

            user = User.objects.get(userId=request.session['userId'])
            event = Event.objects.create(
                userId=user,
                eventType=eventType,
                eventTitle=eventTitle,
                description=description,
                eventposter=eventposter,
                eventDateTime=eventDateTime,
                eventLocation=eventLocation,
                eventFee = eventFee,
                totalAttendees = totalAttendees

            )
            event.save()
            messages.error(request, "Event added.")
            # return redirect("/add_event_form")
    except Exception as e1:
            messages.error(request, "Event not added")

    return redirect("/add_event_form")

def show_events(request):  
    events = Event.objects.all()  
    user = User.objects.get(userId=request.session['userId'])
    return render(request,"organizer/show_events.html",{'events':events, "user": user}) 

def edit_event(request, eventId):  
    event = Event.objects.get(eventId=eventId)  
    return render(request,'organizer/edit_event.html', {'event':event}) 

def update_event_code(request):
    try:
        if request.method == "POST":
            userId = request.session['userId']
            eventId = request.POST.get("eventId")
            eventType = request.POST.get("eventType")
            eventTitle = request.POST.get("eventTitle") 
            description = request.POST.get("description")
            eventDateTime = str(request.POST.get("eventDateTime"))
            eventLocation = request.POST.get("eventLocation")
            eventFee = request.POST.get("eventFee")
            totalAttendees = request.POST.get("totalAttendees")

            user = User.objects.get(userId=request.session['userId'])
            event = Event.objects.get(eventId=eventId)

                
            event.eventType=eventType
            event.eventTitle=eventTitle
            event.description=description
                
            event.eventDateTime=eventDateTime
            event.eventLocation=eventLocation
            event.eventFee = eventFee
            event.totalAttendees = totalAttendees

            
            event.save()
            messages.error(request, "Event Updated.")
            # return redirect("/add_event_form")
    except Exception as e1:
            messages.error(request, "Event not Updated")

    return redirect("/show_events")

def delete_event(request, eventId):
    event = Event.objects.get(eventId=eventId)
    event.delete()
    return redirect("/show_events")

def forgot_password(request):
    return render(request,'homepages/forgot_password.html', {}) 

def reset_password(request):
    try:
        if request.method == "POST":
            
            email = request.POST.get("email")
            user = User.objects.get(email=email) #email exist
            request.session['email'] = email
            print('okkkk')
            message=f'''
'Hi! {user.firstName}  {user.lastName}

Reset your password by following 
this link http://127.0.0.1:8000/change_password/
'''
            send_mail(
                'Campus Event App: Reset your password',                  
                message,         
                settings.EMAIL_HOST_USER,        
                [user.email],       
                fail_silently=False,             
            )
            messages.error(request, "Reset password sent to you mail.")
            


    except Exception as e1:
        messages.error(request, "Invalid emailid.")
        return redirect("/forgot_password")
    
    return redirect("/forgot_password")


def change_password(request):
    return render(request,'homepages/change_password.html', {}) 


def change_password1(request):
    if request.method == "POST":
        email = request.session['email']
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password") 

        if password != confirm_password:
            messages.error(request, "Passwords not match.")
            return redirect("/change_password")
        
        user = User.objects.get(email = email)
        user.password = password
        user.save()
        messages.error(request, "Password changed successfully.")
        return redirect("/change_password")

def attendee_profile(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "attendee/profile.html", {"user": user})

def update_attendee_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        mobile = str(request.POST.get("mobile"))
        course = request.POST.get("course")
        userType = request.POST.get("userType")

        
        user = User.objects.get(email=email)
        user.firstName=firstName
        user.lastName=lastName
        user.email=email
        user.mobile=mobile
        user.course=course
        user.userType=userType
        user.password = password
        
        user.save()
       


    return redirect("/attendee_profile")

def attendee_events(request): 
    current_date = timezone.now().date()  
    events = Event.objects.filter(eventDateTime__gt=current_date)  
    user = User.objects.get(userId=request.session['userId'])
    return render(request,"attendee/show_events.html",{'events':events, "user": user}) 

def make_payment(request):
    if request.method == "POST":
        cardType = request.POST.get("cardType")
        cardNumber = request.POST.get("cardNumber")
        cvv = request.POST.get("cvv")
        expDate = request.POST.get("expDate")
        eventId = request.POST.get("eventId")
        eventFee = request.POST.get("eventFee")
        try:
            # deduct from student account
            account = Account.objects.get(cardType=cardType, cardNumber=cardNumber, cvv= cvv, expDate=expDate)
            account.balance = account.balance - Decimal(str(eventFee))
            account.save()

            # deposit to college account
            account = Account.objects.get(cardNumber='123456789')
            account.balance = account.balance + Decimal(str(eventFee))
            account.save()
            messages.error(request, "Payment success.")

            # add record to registration
            event = Event.objects.get(eventId= eventId)
            user = User.objects.get(userId=request.session['userId'])
            registration = Registration.objects.create(
                user = user,
                event= event

            )
            registration.save()

        except Account.DoesNotExist:
            messages.error(request, "Invalid account details.")
        
        return redirect("/attendee_events")

def attendee_registered_events(request):  
    # attendee
    user = User.objects.get(userId=request.session['userId'])
    registrations = Registration.objects.filter(user=user)
    events = Event.objects.filter(eventId__in=registrations.values_list('event_id', flat=True)).order_by('-eventDateTime')
    return render(request,"attendee/registered_events.html",{'events':events, "user": user})


def organizer_event_registrations(request, eventId):
    user = User.objects.get(userId=request.session['userId'])
    event = Event.objects.get(eventId= eventId)
    registrations = Registration.objects.filter(event=event)

    registered_users = []
    for registration in registrations:
        registered_users.append(registration.user)
    print("okkkk    ")
    return render(request, "organizer/organizer_event_registrations.html", {'user':user, 'event' : event, 'users': registered_users})


def add_feedback(request,eventId):  
    # 
    user = User.objects.get(userId=request.session['userId'])
    return render(request,"attendee/add_feedback.html",{'eventId':eventId, "user": user})


def add_feedback_code(request):
    try:
        if request.method == "POST":
            userId = request.session['userId']
            eventId = request.POST.get("eventId")
            feedback = request.POST.get("feedback") 
            rating = request.POST.get("rating")

            print('userid=', userId, 'eventId=', eventId)
            
            feedback1 = Feedback.objects.create(
                userId=userId,
                eventId=eventId,
                feedback=feedback,
                rating=rating
            )
            feedback1.save()
            messages.error(request, "Feedback added.")
            # return redirect("/add_event_form")
    except Exception as e1:
            messages.error(request, "Event not added")
            print('Error:', str(e1))

    return redirect("/registered_events")


def show_feedback_by_userid_eventid(request,eventId):
    user = User.objects.get(userId=request.session['userId'])
    feedbacks = Feedback.objects.filter(eventId=eventId, userId=request.session['userId'])
    return render(request, 'attendee/show_feedback_by_userid_eventid.html', {'user': user,'feedbacks': feedbacks})

'''
def show_all_feedbacks_by_userid(request):
    user = User.objects.get(userId=request.session['userId'])
    feedbacks = Feedback.objects.filter(userId=request.session['userId'])
    return render(request, 'attendee/show_all_feedbacks_by_userid.html', {'user': user,'feedbacks': feedbacks})
'''

def show_all_feedbacks_by_userid(request):
    user = User.objects.get(userId=request.session['userId'])
    
    registrations = Registration.objects.filter(user=user)
    events = Event.objects.filter(eventId__in=registrations.values_list('event_id', flat=True)).order_by('-eventDateTime')
  
    event_feedback_data = []  

    
    for event in events:
        
        feedbacks = Feedback.objects.filter(eventId=event.eventId)

        
        event_feedback_entry = {
            'event': event,
            'feedbacks': feedbacks
        }

        
        event_feedback_data.append(event_feedback_entry)

    return render(request, 'attendee/show_all_feedbacks_by_userid.html', {'user': user, 'event_feedback_data': event_feedback_data})


def show_feedbacks_organizer(request):
    user = User.objects.get(userId=request.session['userId'])
    
    events = Event.objects.filter(userId=user).order_by('-eventDateTime')
  
    event_feedback_data = []  

    
    for event in events:
        
        feedbacks = Feedback.objects.filter(eventId=event.eventId)

        
        event_feedback_entry = {
            'event': event,
            'feedbacks': feedbacks
        }

        
        event_feedback_data.append(event_feedback_entry)

    return render(request, 'organizer/show_feedbacks_by_organizer.html', {'user': user, 'event_feedback_data': event_feedback_data})



    