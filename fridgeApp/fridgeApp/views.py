from .forms import RegistrationForm, UserCreationForm, AddItemForm

from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import datetime
import logging

from .models import Items

logger = logging.getLogger('__name__')

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


def register(request):
    if request.method == 'GET':
        logger.info('Get request to register page')
        form = RegistrationForm()
        return render(request, template_name='fridgeApp/register.html', context={'form': form})
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


def password_reset(request):
    if request.method == "GET":
        return render(request, template_name="fridgeApp/password_reset.html")
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

        return render(request, template_name="fridgeApp/add_user.html", context=context)

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


def list_all_items(request):
    if request.method == "GET":
        context = {
            "items": Items.objects.all().order_by("-created_on"),
        }
        print([item.days_remaining().days < 4  for item in context["items"]])
        return render(request, template_name="fridgeApp/list_items.html", context=context)


def add_item(request):
    if request.method == "GET":
        form = AddItemForm()
        context = {
            "form": form,
        }
        return render(request, template_name="fridgeApp/add_item.html", context=context)

    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item Added")
            return HttpResponseRedirect(redirect_to=reverse('list_all_items'))


def delete_items(request, id):
    item = Items.objects.get(id=id)
    item.delete()
    return HttpResponseRedirect(redirect_to=reverse("list_all_items"))
