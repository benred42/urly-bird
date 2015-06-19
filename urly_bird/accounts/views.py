from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from accounts.forms import UserForm

# Create your views here.
def register_rater(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            password = user.password
            user.set_password(password)
            user.save()

            user = authenticate(username=user.username,
                                password=password)

            login(request, user)

            messages.add_message(
                request,
                messages.SUCCESS,
                "Welcome, {}. You have successfully created an account and are now logged in".format(user.username))

            return redirect("all_bookmarks")
    else:
        user_form = UserForm()
    return render(request, "registration/register.html", {'user_form': user_form})
