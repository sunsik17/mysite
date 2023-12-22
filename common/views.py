from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import render, redirect

from common.forms import SignUpForm
from pybo import views


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'common/signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('index')