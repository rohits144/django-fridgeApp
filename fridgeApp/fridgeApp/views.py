from .forms import RegistrationForm, UpdateProfileForm, UserCreationForm

from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import logging

logger = logging.getLogger('__name__')

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == 'GET':
        logger.info('Get request to register page')
        form = RegistrationForm()
        return render(request, template_name='effort_tracker/register.html', context={'form': form})
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully, Please log in now')
            return HttpResponseRedirect(redirect_to=reverse('login'))
        else:
            logger.info('Incorrect data provided')
            messages.error(request, form.errors)
            return HttpResponseRedirect(redirect_to=reverse('register'))


def profile(request):
    if request.user.is_authenticated:
        try:
            curr_exp = "{:.1f} yr".format(float(request.user.profile.joining_exp) + float(
                ((datetime.now().date() - request.user.profile.site_joining_date).days / 30) / 12))
        except Exception as e:
            curr_exp = 0.0

        try:
            if request.user.profile.display_pic.url == '/media/False':
                display_pic = "/static/dpp.jpg"
            else:
                display_pic = request.user.profile.display_pic.url
        except ValueError:
            display_pic = "/static/dpp.jpg"

        print("@@@@@", display_pic)
        return render(request, template_name='effort_tracker/profile.html',
                      context={'user': request.user, 'curr_exp': curr_exp, 'display_pic': display_pic})
    else:
        messages.warning(request, 'First login to view your profile')
        return HttpResponseRedirect(redirect_to=reverse('login'))


def update_profile(request):
    if request.user.is_authenticated and request.method == "GET":
        form = UpdateProfileForm(instance=request.user.profile,
                                 initial={'name': (request.user.first_name + " " + request.user.last_name),
                                          'site_joining_date': request.user.profile.site_joining_date,
                                          'joining_exp': request.user.profile.joining_exp,
                                          })
        context = {
            "form": form
        }
        return render(request, template_name="effort_tracker/update_profile.html", context=context)

    elif request.user.is_authenticated and request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("****************", bool(request.user.profile.display_pic) == False)
            if form.cleaned_data["display_pic"] is None and request.user.profile.display_pic.url == "/media/False":
                print("DP none true", request.user.profile.display_pic.url)
                form.cleaned_data["display_pic"] = request.user.profile.display_pic.url

            form.cleaned_data["joining_exp"] = request.user.profile.joining_exp
            form.cleaned_data["site_joining_date"] = request.user.profile.site_joining_date
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            logger.info("task updated")
            logger.info("Profile update for - {}".format(request.user.username))
            messages.info(request, "Profile details update")
            return HttpResponseRedirect(redirect_to=reverse("profile"))

        else:
            messages.error(request, "error in form")
            return HttpResponseRedirect(redirect_to=reverse("update_profile"))


def password_reset(request):
    if request.method == "GET":
        return render(request, template_name="effort_tracker/password_reset.html")
    if request.method == "POST":
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            user_obj = User.objects.get(username=username)
        except ObjectDoesNotExist as e:
            logger.error("User with username - {}".format(username))
            messages.error(request, "User not found")
            return HttpResponseRedirect(redirect_to=reverse('password_reset'))
        else:
            if check_password(old_password, user_obj.password):
                if new_password == confirm_password:
                    user_obj.set_password(new_password)
                    user_obj.save()
                    messages.success(request, "Password reset done")
                    return HttpResponseRedirect(redirect_to=reverse('login'))
                else:
                    messages.error(request, "new password and confirm password did not match, try again")
                    return HttpResponseRedirect(redirect_to=reverse('password_reset'))
            else:
                messages.error(request, "Check if Old password is correct? ")
                return HttpResponseRedirect(redirect_to=reverse('password_reset'))


def add_user(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {
            "form": form,
        }

        return render(request, template_name="effort_tracker/add_user.html", context=context)

    elif request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            account_type = request.POST.get('account_type')
            if account_type == "Bosch Associate":
                bosch_joining_date = request.POST.get('bjd')
                exp_on_joining_date = request.POST.get('ejd')
                user_obj = User.objects.create_user(username=username, email=email, password=password2)
                user_obj.profile.site_joining_date = bosch_joining_date
                user_obj.profile.joining_exp = exp_on_joining_date
                user_obj.profile.save()
                messages.success(request, "User Created Successfully")
                return HttpResponseRedirect(reverse('profile'))
            elif account_type == "SITE Team Lead":
                User.objects.create_user(username=username, email=email, password=password2)
                messages.success(request, "User Created Successfully")
                return HttpResponseRedirect(reverse('profile'))
        else:
            messages.error(request, "Password1 and password2 does not match, please try again")
            return HttpResponseRedirect(reverse('add_user'))
