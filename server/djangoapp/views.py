from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cloudant, get_dealer_reviews_from_cloudant, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index_view(request):
    ctx = {}
    return render(request, "djangoapp/index.html", context=ctx)

# Create an `about` view to render a static about page
# def about(request):
# ...
def about_view(request):
    ctx = {}
    return render(request, "djangoapp/about.html", context=ctx)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact_view(request):
    ctx = {}
    return render(request, "djangoapp/contact.html", context=ctx)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_view(request):
    ctx = {}
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return redirect("djangoapp:index")
    else:
        return redirect("djangoapp:index")

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_view(request):
    ctx = {}

    logout(request)
    return redirect("djangoapp:index")
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def signup_view(request):
    ctx = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", ctx)
    elif request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        password = request.POST["password"]
        
        try:
            User.objects.get(username=username)
            user_exists = True
        except:
            user_exists = False
        
        if not user_exists:
            newuser = User.objects.create_user(username=username, first_name=fname, last_name=lname, password=password)
            login(request, newuser)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", ctx)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://a8903b5f.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cloudant(url, state="")
        context["dealerships"] = dealerships
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        url = "https://a8903b5f.eu-gb.apigw.appdomain.cloud/api/"
        reviews = get_dealer_reviews_from_cloudant(url + "review", dealerId=dealerId)
        context["reviews"] = reviews
        dealer = get_dealers_from_cloudant(url + "dealership", dealerId=dealerId)
        context["dealer"] = dealer[0]
        return render(request, "djangoapp/dealer_details.html", context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealerId):
    context = {}
    if request.method == "POST" and request.user.is_authenticated:
        #probably temporary i would hope vvv
        review = dict()
        review["id"] = 33
        review["name"] = "John Doe"
        review["dealership"] = 3
        review["review"] = "I cannot say how much I hated the service. Blow it all up."
        review["purchase"] = True
        review["purchase_date"] = datetime.utcnow().isoformat()
        review["car_make"] = "Audi"
        review["car_model"] = "A6"
        review["car_year"] = 1999

        json_payload = dict()
        json_payload["review"] = review

        res = post_request("https://a8903b5f.eu-gb.apigw.appdomain.cloud/api/review", json_payload, dealerId=dealerId)
        return HttpResponse(res)
    if request.method == "GET":
        return HttpResponse("Ayo its here")