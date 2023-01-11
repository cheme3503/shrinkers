from django.contrib import admin
from .models import PayPlan, Users, ShortenedUrls, Statistic

# Register your models here.

admin.site.register(PayPlan)
admin.site.register(Users)
admin.site.register(ShortenedUrls)
admin.site.register(Statistic)

