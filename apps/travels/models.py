# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login.models import User
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Travels(models.Model):
    destination = models.CharField(max_length=100)
    User = models.ForeignKey(User, related_name="books")
    def __str__(self):
        return self.title

class ReviewManager(models.Manager):
    def validate_review(self, post_data):
        errors = []

        if len(post_data['title']) < 1 or len(post_data['review']) < 1:
            errors.append('fields are required')
        if not "user" in post_data and len(post_data['new_user']) < 3:
            errors.append('new user names must 3 or more characters')

        if "user" in post_data and len(post_data['new_user']) > 0 and len(post_data['new_author']) < 3:
            errors.append('new user names must 3 or more characters')
        if not int(post_data['rating']) > 0 or not int(post_data['rating']) <= 5:
            errors.append('invalid rating')
        return errors

    def create_review(self, clean_data, user_id):
        # retrive or create user
        the_user = None
        if len(clean_data['new_user']) < 1:
            the_user = User.objects.get(id=int(clean_data['user']))
        else:
            the_user = User.objects.create(name=clean_data['new_user'])
        # retirive or create travels
        the_travels = None
        if not Travels.objects.filter(title=clean_data['title']):
            the_travels = Travels.objects.create(
                title=clean_data['title'], user=the_user
            )
        else:
            the_travels = Travels.objects.get(title=clean_data['title'])
        self.create(
            planned = clean_data['planned'],
            description = clean_data['description'],
            travels = the_travels,
            user = User.objects.get(id=user_id)
        )

    def recent_and_not(self):
        '''
        returns a tuple with the zeroeth index containing query for 3 most recent reviews, and the first index
        containing the rest
        '''
        return (self.all().order_by('-created_at')[:3], self.all().order_by('-created_at')[3:])

class destination(models.Model):
    travel_date_to = models.DateTimeField(auto_now_add=True)
    travel_date_from = models.DateTimeField()
    planned_by = models.ForeignKey(User, related_name="reviews_left")
    description = ReviewManager()
    def __str__(self):
        return "Book: {}".format(self.book.title)