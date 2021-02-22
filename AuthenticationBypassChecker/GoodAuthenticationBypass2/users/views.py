from django.shortcuts import render, redirect
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

        ### original code
        if form.is_valid():
            user = User.objects.get(nickname=form.cleaned_data['user'])
            if user.user_answer == form.cleaned_data['answer']: # 입력한 답이 가입했을 때 답이랑 같은지 확인
                new_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                messages.info(request, 'Your new password is ' + new_password)
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                return HttpResponse('Wrong answer')
        else:
            return redirect(reverse('findpassword'))