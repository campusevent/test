"""CampusEventsManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from campus_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('user_registration/', views.user_registration),
    path('add_user_registration/', views.add_user_registration),
    path('validate_user_login/', views.validate_user_login),
    path('logout/', views.logout),
    path('profile/', views.profile),
    path('home/', views.home),
    path('attendee_home/', views.attendee_home),
    path('update_user/', views.update_user),
    path('add_event_form/', views.add_event_form),
    path('add_event_code/', views.add_event_code),
    path('show_events/', views.show_events),
    path('edit_event/<int:eventId>', views.edit_event),
    path('update_event_code/', views.update_event_code),
    path('delete_event/<int:eventId>', views.delete_event),
    path('forgot_password/', views.forgot_password),
    path('reset_password/', views.reset_password),
    path('change_password/', views.change_password),
    path('change_password1/', views.change_password1),
    path('attendee_profile/', views.attendee_profile),
    path('update_attendee_user/', views.update_attendee_user),
    path('attendee_events/', views.attendee_events),
    path('make_payment/', views.make_payment),
    path('registered_events/', views.attendee_registered_events),
    path('organizer_event_registrations/<int:eventId>', views.organizer_event_registrations),
    path('add_feedback/<int:eventId>', views.add_feedback),
    path('add_feedback_code/', views.add_feedback_code),
    path('show_feedback_by_userid_eventid/<int:eventId>', views.show_feedback_by_userid_eventid),
    path('show_all_feedbacks_by_userid/', views.show_all_feedbacks_by_userid),
    path('show_feedbacks_organizer/', views.show_feedbacks_organizer),
]
