# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Destination, User, Travels
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'recent': Travels.objects.recent_and_not()[0],
        'more': Travels.objects.recent_and_not()[1]
    }
    return render(request, 'travels/index.html', context)

def add(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, 'travels/add.html', context)

def show(request, destination_id):
    context = {
        'destination': Destination.objects.get(id=destination_id)
    }
    return render(request, 'travels/show.html', context)

def create(request):
    errs = Travels.objects.validate_destination(request.POST)
    if errs:
        for e in errs:
            messages.error(request, e)
    else:
        Travels.objects.create_destination(request.POST, request.session['user_id'])
    return redirect('/destination')

def create_additional(request, destination_id):
    print destination_id, type(destination_id)
    the_destination = destination.objects.get(id=destination_id)
    new_destination_data = {
        'destination': the_destination.title,
        'user': the_destination.user.id,
        'travel_start_date': request.POST['start_date'],
        'travel_end_date': request.POST['end_date'],
        'new_user': ''
    }
    errs = Review.objects.validate_review(new_destination_data)
    if errs:
        for e in errs:
            messages.error(request, e)
    else:
        Destination.objects.create_destination(new_destination_data, request.session['user_id'])
    return redirect('/travels/' + destination_id)