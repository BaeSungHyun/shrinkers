from django.contrib import admin
from shortener.models import PayPlan, Users, Organization

# Register your models here.

# register 'PayPlan' in admin site
admin.site.register(PayPlan)
admin.site.register(Users)
admin.site.register(Organization)
