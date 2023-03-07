from django.db import models

import string
import random

# Create your models here.

class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True) # update time
    create_at = models.DateTimeField(auto_now_add=True) # create time once

# Customizing User model provided by Django

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Inheriting 'AbstractUser' ables to customize User Model. Don't forget to point to AUTH_USER_MODEL
# Creates in existing 'User' table (One Table).
# If you customized in first place, this way more convenient.
class Users(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)

# Above : create 'shortener_users'. Below : create 'auth_user' and seperate 'UserDetail' table.
# There can be only one User.

# Creates seperate table (Two table). Don't need AUTO_USER_MODEL (I think)
# If you didn't customize 'User' in first place, then using seperate table better.
# class UserDetail(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE)
#     pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING)


class ShortenerUrls(models.Model):
    class UrlCreatedVia(models.TextChoices): # class for creating enumerating text choices
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)]).lower())
    
    nick_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=6, default=rand_string)
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)