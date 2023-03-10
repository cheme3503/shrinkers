from django.db import models
from django.contrib.auth.models import User as U
import string
import random
from django.contrib.gis.geoip2 import GeoIP2
from datetime import datetime,timedelta
import itertools
from typing import Dict
from django.db.models.base import Model
from .models_utils import dict_filter, dict_slice, location_finder
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.
class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

class Organization(models.Model):
    class Industries(models.TextChoices):
        PERSONAL = "personal"
        RETAIL = "retail"
        MANUFACTURING = 'manufacturing'
        IT = 'it'
        OTHERS = 'others'

    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=15, choices = Industries.choices, default = Industries.OTHERS)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Users(models.Model):
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    telegram_username = models.CharField(max_length=100, null=True, blank=True)
    url_count = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank = True)

class EmailVerification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, null=True)
    verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add=True)

class Categories(models.Model):
    name = models.CharField(max_length = 100)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ShortenedUrls(models.Model):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()

    def rand_letter():
        str_pool = string.ascii_letters
        return random.choice(str_pool).lower()

    nick_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, null=True, blank=True)
    prefix = models.CharField(max_length=50, default=rand_letter)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE)
    target_url = models.CharField(max_length=2000)
    click = models.BigIntegerField(default=0)
    shortened_url = models.CharField(max_length = 6, default=rand_string)
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    expired_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['prefix','shortened_url'])
        ]

    def clicked(self):
        self.click += 1
        self.save()
        return self

class Schedules(models.Model):
    job_name = models.CharField(max_length=50)
    flag_name = models.CharField(max_length=50)
    value = models.IntegerField(default=0)

class Statistic(models.Model):
    class ApproachDevice(models.TextChoices):
        PC = 'pc'
        MOBILE = 'mobile'
        TABLET = 'table'

    shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    web_browser = models.CharField(max_length=50)
    device = models.CharField(max_length=6, choices = ApproachDevice.choices)
    device_os = models.CharField(max_length=30)
    country_code = models.CharField(max_length=2, default="XX")
    country_name = models.CharField(max_length=100, default="UNKNOWN")
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    custom_params = models.JSONField(null=True)

    def record(self, request, url:ShortenedUrls, params: Dict):
        self.shortened_url = url
        self.ip = request.META["REMOTE_ADDR"] #HttpRequest.META ??? available HTTP header??? ?????????.
                                              #Remot_ADDR??? clien??? IP address??? ?????? key ??????.
        self.web_browser = request.user_agent.browser.family
        self.device = (self.ApproachDevice.MOBILE
                       if request.user_agent.is_mobile
                       else self.ApproachDevice.TABLE
                       if request.user_agent.is_tablet
                       else self.ApproachDevice.PC
                       )
        self.device_os = request.user_agent.os.family
        t = TrackingParams.get_tracking_param(url.id) #list of tuple ??????
        if params:
            self.custom_params = dict_slice(dict_filter(params, t), 5) #Dictionary ????????? params ??? key??????, t??? ?????????,
                                                                   # dictionary ????????? ????????????, 5??? item??? slicing
        try:
            country = GeoIP2().country(self.ip)
            self.country_code = country.get("country_code", "XX")
            self.country_name = country.get("country_name", "UNKONWN")
        except:
            pass

        url.clicked()
        self.save()


class TrackingParams(models.Model):
    shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
    params = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod      #model instance ??? customizing ??? ??? ???????????? decorator
    def get_tracking_param(cls, shortened_url_id):
        return cls.objects.filter(shortened_url_id=shortened_url_id).values_list("params", flat=True)
#         #values_list(*fields, flat=Falst, named=False)??? values()??? ????????????, values()??? dictionary??? ??????????????? ??????, tuple???
#         #?????????.

class BackOfficeLogs(models.Model):
    endpoint = models.CharField(max_length=200, blank=True, null=True)
    body = models.JSONField(null=True)
    method = models.CharField(max_length=200, blank = True, null = True)
    user_id = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=30, blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DailyVisitors(models.Model):
    visit_date = models.DateField()
    visits = models.IntegerField(default = 0)
    totals = models.IntegerField(default=0)
    last_updated_on = models.DateTimeField(auto_now=True)

class JobInfo(models.Model):
    class JOB_STATUS(models.TextChoices):
        WAIT = 'wait'
        RUN = 'run'
        OK = 'ok'
        ERROR = 'error'

    job_id = models.CharField(max_length=255)
    user_id = models.IntegerField(null= True)
    additional_info = models.JSONField(null=True)
    status = models.CharField(max_length=6, choices=JOB_STATUS.choices, default=JOB_STATUS.WAIT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)