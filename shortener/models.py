from django.db import models

import string
import random

# Create your models here.

# class PayPlan(models.Model):
#     name = models.CharField(max_length=20)
#     price = models.IntegerField()
#     updated_at = models.DateTimeField(auto_now=True) # update time
#     create_at = models.DateTimeField(auto_now_add=True) # create time once

# Customizing User model provided by Django

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Inheriting 'AbstractUser' ables to customize User Model. Don't forget to point to AUTH_USER_MODEL
# Creates in existing 'User' table (One Table).
# If you customized in first place, this way more convenient.
# class Users(AbstractUser):
#     full_name = models.CharField(max_length=100, null=True)
#     pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)

# Above : create 'shortener_users'. Below : create 'auth_user' and seperate 'UserDetail' table.
# There can be only one User.

# Creates seperate table (Two table). Don't need AUTO_USER_MODEL (I think)
# If you didn't customize 'User' in first place, then using seperate table better.
# class UserDetail(models.Model):
#     user = models.OneToOneField(Users, on_delete=models.CASCADE)
#     pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING)


# class ShortenerUrls(models.Model):
#     class UrlCreatedVia(models.TextChoices): # class for creating enumerating text choices
#         WEBSITE = "web"
#         TELEGRAM = "telegram"

#     def rand_string():
#         str_pool = string.digits + string.ascii_letters
#         return ("".join([random.choice(str_pool) for _ in range(6)]).lower())
    
#     nick_name = models.CharField(max_length=100)
#     created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
#     target_url = models.CharField(max_length=2000)
#     shortened_url = models.CharField(max_length=6, default=rand_string)
#     created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

class PayPlan(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now = True)
    create_at = models.DateTimeField(auto_now_add=True)

class Organization(models.Model):
    class Industries(models.TextChoices):
        PERSONAL = "personal"
        RETAIL = "retail"
        MANUFACTURING = "manufacturing"
        IT = "it"
        OTHERS = "others"
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=15, choices=Industries.choices, default=Industries.OTHERS)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True) # gets pay_plan_id
    updated_at = models.DateTimeField(auto_now = True)
    create_at = models.DateTimeField(auto_now_add=True)

class Users(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) # AUTH_USER_MODEL 이랑 1:1 mapping. Settings 에서 지워줘야함
    full_name = models.CharField(max_length=100, null=True)
    # organization 만들면 유료, 안 만들면 무료
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True) 

class EmailVerification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True) # null=True 는 ForeignKey에서는 안좋음
    # index가 섞인다고 해야되나..?
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now = True)
    create_at = models.DateTimeField(auto_now_add=True)

class ShortenedUrls(models.Model):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"
    
    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()
    
    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True)
    prefix = models.CharField(max_length=50) # /a/1234, /b/1234 ... 기준을 하나 더 만들어줌. 더 많은 url
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    shortend_url = models.CharField(max_length=6, default=rand_string)    
    create_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    expired_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)





