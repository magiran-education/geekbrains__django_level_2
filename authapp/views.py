from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from authapp.models import User
from basketapp.models import Basket
from django.db import transaction


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    title = f'Для активации учётной записи {user.username} пройдите по ссылке'
    message = f'Для подтверждения учётной записи {user.username} пройдите поссылке: {settings.DOMAIN_NAME}' \
              f'{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user: {e.args}')
        return HttpResponseRedirect(reverse('index'))


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, f'Письмо с валидацией аккаунта отправлено на почту {user.email}.')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.success(request, f'Ошибка отправки письма с валидацией аккаунта.')
                return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'authapp/register.html', context)


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
        user_profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=user.userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        user_form = UserProfileForm(instance=user)
        user_profile_form = UserProfileEditForm(instance=user.userprofile)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'baskets': Basket.objects.filter(user=user),
    }
    return render(request, 'authapp/profile.html', context)


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     context = {
#         'form': form,
#         'baskets': Basket.objects.filter(user=user),
#     }
#     return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# @transaction.atomic
# def edit(request):
#     # title = 'Редактирование'
#
#     if request.method == 'POST':
#         edit_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)

