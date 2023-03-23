from rest_framework.permissions import OR
from shortener.models import Organization, PayPlan
from ninja import Schema
from django.contrib.auth.models import User as U
from ninja.orm import create_schema

OrganizationSchema = create_schema(Organization, exclude=["industry"]) # 이렇게 하면 굳이 구구절절히 아래처럼 안써줘도 됨

class Users(Schema): # 이런 model 형태로 return 해라!
    id: int
    full_name: str = None
    organization: OrganizationSchema = None # ForeignKey랑 똑같은 이름!

class TelegramUpdateSchema(Schema):
    username: str