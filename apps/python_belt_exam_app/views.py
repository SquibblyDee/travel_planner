#import needed django modules
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth

#import bcrypt
import bcrypt

#  import our db
from .models import *

#This is our index page and contains login and registration forms
def loginandreg(request):
    return render(request,'python_belt_exam_app/loginandreg.html')

#Processes information from the registration form
def process_register(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
        # if the errors object is empty, that means there were no errors!
        # add our new record to the table , push what we need to session,
        # and redirect to /success to render our final page
        User.objects.create(first_name=request.POST['input_first_name'], last_name=request.POST['input_last_name'], email=request.POST['input_email'], password=bcrypt.hashpw(request.POST['input_password'].encode('utf8'), bcrypt.gensalt()))
        query = User.objects.filter(email=request.POST['input_email']).values('id', 'email')
        for row in query:
            request.session['isloggedin'] = row['id']
            request.session['id'] = row['id']
            request.session['useremail'] = row['email']
        request.session['error'] = ""
        request.session['welcomename'] = request.POST['input_first_name']
        request.session['welcomemessage'] = 'Successfully registered!'
        return redirect('/travels')

#Processes information from the login form
def process_login(request, methods=['POST']):
    # Query the data we need
    query = User.objects.all().values('id', 'email', 'first_name', 'password')
    # Iterate through query until we find user email then verify password is legit
    for row in query:
        if row['email'] == request.POST['login_email'] and bcrypt.checkpw(request.POST['login_password'].encode(), row['password'].encode()): 
            request.session['error'] = ""
            request.session['useremail'] = row['email']
            request.session['id'] = row['id']
            request.session['isloggedin'] =  row['id']
            request.session['welcomename'] = row['first_name']
            request.session['welcomemessage'] = 'Successfully logged in!'
            return redirect('/travels')
    request.session['error'] = "• Try again"
    return redirect('/')

#############################EVERYTHING ABOVE HERE IS LOGIN ####################################################

#This is the landing page that the user arrives at after registering or logging in
def landing(request):
    # If the user has a isLoggedin session
    query = User.objects.filter(id=request.session['isloggedin']).values('id', 'email')
    if 'isloggedin' in request.session:
        for row in query:
            if request.session['isloggedin'] == row['id'] and request.session['useremail'] == row['email']:
                me = User.objects.get(id=request.session['isloggedin'])
                context = {
                    "alltrips" : Trip.objects.exclude(all_users=request.session['isloggedin']),
                    "mytrips" : me.all_trips.all(),
                }
                return render(request,'python_belt_exam_app/landing.html', context)
    else:
        return redirect('/')


def addtrip(request):
    return render(request, 'python_belt_exam_app/addtrip.html')

def processtrip(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Trip.objects.basic_validator2(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/addtrip')
    else:
        me = User.objects.get(id=request.session['isloggedin'])
        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], trip_users=me, datefrom=request.POST['datefrom'], dateto=request.POST['dateto'])
        trip = Trip.objects.last()
        print("TRIP ID: ", trip.id)
        print("ME: ", me.id)
        # THIS ADDS THE STUFF TO OUR LINKING TABLE
        trip.all_users.add(me)
        return redirect('/travels')

def show_process(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context={
        "me" : User.objects.get(id=request.session['isloggedin']),
        "this_trip": Trip.objects.filter(id=trip_id),
        "trip_members": trip.all_users.exclude(id=trip.trip_users.id),
    }
    print(context)
    return render(request,'python_belt_exam_app/view.html', context)

def join_process(request, trip_id):
    me = User.objects.get(id=request.session['isloggedin'])
    trip = Trip.objects.get(id=trip_id)
    trip.all_users.add(me)
    context = {
                "alltrips" : Trip.objects.exclude(all_users=request.session['isloggedin']),
                "mytrips" : me.all_trips.all(),
            }
    #return redirect('/travels')
    return render(request,'python_belt_exam_app/all.html', context)

def cancel_process(request, trip_id):
    me = User.objects.get(id=request.session['isloggedin'])
    trip = Trip.objects.get(id=trip_id)
    trip.all_users.remove(me)
    return redirect('/travels')

def delete_process(request, trip_id):
    b = Trip.objects.get(id=trip_id)
    b.delete()
    return redirect('/travels')

# Clears out session / logs out the user
def logout(request):
    auth.logout(request)
    return redirect('/')