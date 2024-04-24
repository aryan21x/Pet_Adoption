from django.db import models
from django.views.generic import TemplateView
from django.shortcuts import render ,redirect
import mysql.connector
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .backends import MySQLBackend

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="rootnew",
    password="1234",
    database="project" 
)

def welcome(request):
    return render(request, 'welcome.html')


class HomeView(TemplateView):
    template_name = 'homeView.html'

    # Define login view
def user_login2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against MySQL database
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_table WHERE username = %s AND password = %s", (username, password))
        user_row = cursor.fetchone()

        if user_row:
            # Create Django user object
            #user = authenticate(request, username=username, password=password)
            if user_row is not None:
                return render(request, 'welcome.html', {'username': username})
        else:
            #Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against MySQL database
        user = MySQLBackend().authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return render(request, 'welcome.html', {'username': username})
        else:
            # Invalid login
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    
    # GET request or invalid form submission
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')
