from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import BaseUser, Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import Error, IntegrityError



@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

# def signup(request):
#     return render(request,"users/registration.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("redirect")
    elif request.method == "POST":
        login_email = request.POST.get("login-email")
        login_password = request.POST.get("login-password")
        
        user = authenticate(request, email=login_email, password=login_password)
        if user is not None:
            login(request, user)
            if user.user_type == "USER":
                return redirect("/")
            elif user.user_type == "SUPERUSER":
                return redirect("/admin")
            else:
                return HttpResponse("Please contact admin.")
        else:
            messages.error(request, "Login Credentials Failed. Check your email and password.")
            return redirect("/login")
    else:
        return render(request, "users/login.html")


def signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get("login-email")
            password = request.POST.get("login-password")
            user_type = "USER"
            Profile.objects.create(
                username=request.POST.get("username"),
                email=email,
                bio=request.POST.get('bio'),
                place=request.POST.get('place')
            )
            BaseUser.objects.create_user(email=email, password=password, user_type=user_type)
            messages.success(request, "Account Created Successfully.")
            return redirect('/login')
        except IntegrityError as e:
            print(e)
            messages.error(request, "The email might have been used already. If you haven't registered with us, "
                                    "retry with the same email or try with a different email.")
        except Error:
            messages.error(request, "Something went wrong. Contact admin or try again later.")

    return render(request, "users/registration.html")
    


