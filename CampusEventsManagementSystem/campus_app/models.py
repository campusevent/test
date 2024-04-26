from django.db import models

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    userPic = models.CharField(max_length=150)
    registerDate = models.DateField(auto_now_add=True)
    USER_TYPES = (
        ('Organizer', 'Organizer'),
        ('Attendee', 'Attendee'),
    )
    userType = models.CharField(max_length=50, choices=USER_TYPES)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Event(models.Model):
    eventId = models.AutoField(primary_key=True)
    eventAddDate = models.DateField(auto_now_add=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    eventType = models.CharField(max_length=50)
    eventTitle = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    eventposter = models.CharField(max_length=150)
    eventDateTime = models.DateTimeField()
    eventLocation = models.CharField(max_length=200)
    eventFee = models.FloatField()
    totalAttendees = models.IntegerField()

    def __str__(self):
        return self.eventTitle


class Account(models.Model):
    accountNumber = models.CharField(primary_key=True, max_length=20)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    address = models.TextField()
    openDate = models.DateField()
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    cardType = models.CharField(max_length=50)
    cardNumber = models.CharField(max_length=50)
    cvv = models.CharField(max_length=5)
    expDate = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Registration(models.Model):
    registerId = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registrationDate = models.DateField(auto_now_add=True)

class Feedback(models.Model):
    feedbackId = models.AutoField(primary_key=True)
    eventId = models.IntegerField()
    userId = models.IntegerField()
    feedbackDate = models.DateField(auto_now_add=True)
    feedback = models.CharField(max_length=300)
    rating = models.IntegerField()

    def __str__(self):
        return f"Feedback {self.feedbackId} - Event {self.eventId} - User {self.userId}"