from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from .models import User

from .forms import UserCreationForm, FindPasswordForm

import random, string

def dashboard(request):
    return render(request, 'users/dashboard.html')

class CreateUser(View):
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}

        return render(request, 'users/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            request.session['user'] = User.objects.get(nickname=form.cleaned_data['nickname']).id #세션 저장
            login(request, user)
        return HttpResponseRedirect(reverse('dashboard'))

class FindPassword(View):
    def get(self, request):
        form = FindPasswordForm()
        context = {"form": form}

        return render(request, 'users/findpassword.html', context)

    def post(self, request):
        form = FindPasswordForm(request.POST)

        ### is_valid를 안쓰는 취약한 코드 (Intercept해서 Auth Bypass가 가능)
        user_ref = form.data['user']
        user = User.objects.get(pk=user_ref)
        param_names = request.POST.keys()
        user_answer = {}

        for param_name in param_names:
            if 'answer' in param_name:
                user_answer[param_name] = request.POST[param_name]

        if 'answer' in user_answer and user_answer['answer'] != user.user_answer:
            return HttpResponse('Wrong answer')
        else:
            new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            messages.info(request, 'Your new password is ' + new_password)
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(reverse('login'))
