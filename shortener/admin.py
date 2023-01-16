from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(PayPlan)
admin.site.register(Users)
admin.site.register(ShortenedUrls)
admin.site.register(Statistic)
admin.site.register(Schedules)
admin.site.register(BackOfficeLogs)
admin.site.register(JobInfo)