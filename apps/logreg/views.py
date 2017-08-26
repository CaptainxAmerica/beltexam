# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
# Belt Reviewer solutions
def index(request):
    return render(request, 'logreg/index.html')

def register(request):
    print request.POST
    errs = User.objects.validate_registration(request.POST)
    if errs:
        for e in errs:
            messages.error(request, e)
    else:
        # make a user
        new_user = User.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        messages.success(request, "Thank you {} for registering".format(new_user.username))
    return redirect('/')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Login complete!")
    return HttpResponseRedirect(reverse("review:index"))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'logreg/success.html', context)

def show(request, user_id):
    user = User.objects.get(id=user_id)
    unique_ids = user.reviews_left.all().values("travels").distinct()
    unique_books = []
    for book in unique_ids:
        unique_books.append(Book.objects.get(id=book['travels']))
    context = {
        'user': user,
        'destination_description': destination_description
    }
return render(request, 'logreg/show.html', context)