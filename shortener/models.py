from django.db import models
from django.contrib.auth.models import User as U
import string
import random
from django.contrib.gis.geoip2 import GeoIP2
from datetime import datetime,timedelta
import itertools
from typing import Dict
from django.db.models.base import Model
# from .models_utils import dict_filter, dict_slice, location_finder
from django.utils import timezone

# from django.contrib.auth.models import User

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
    device_os = models.CharField(max_length=6)
    country_code = models.CharField(max_length=2, default="XX")
    country_name = models.CharField(max_length=100, default="UNKNOWN")
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(default = datetime.now() - timedelta(days=7))
    # custom_params = models.JSONField(null=True)

    def record(self, request, url:ShortenedUrls):
        self.shortened_url = url
        self.ip = request.META["REMOTE_ADDR"] #HttpRequest.META 는 available HTTP header를 반환함.
                                              #Remot_ADDR은 clien의 IP address에 대한 key 값임.
        self.web_browser = request.user_agent.browser.family
        self.device = (self.ApproachDevice.MOBILE
                       if request.user_agent.is_mobile
                       else self.ApproachDevice.TABLE
                       if request.user_agent.is_tablet
                       else self.ApproachDevice.PC
                       )
        self.device_os = request.user_agent.os.family
        # t = TrackingParams.get_tracking_param(url.id) #list of tuple 반환
        # self.custom_params = dict_slice(dict_filter(params, t), 5) #Dictionary 형태의 params 의 key값이, t에 있으면,
                                                                   # dictionary 형태로 반환하여, 5개 item을 slicing
        try:
            country = GeoIP2().country(self.ip)
            self.country_code = country.get("country_code", "XX")
            self.country_name = country.get("country_name", "UNKONWN")
        except:
            pass
        url.clicked()
        self.save()


# class TrackingParams(models.Model):
#     shortened_url = models.ForeignKey(ShortenedUrls, on_delete=models.CASCADE)
#     params = models.CharField(max_length=20)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     @classmethod      #model instance 를 customizing 할 때 사용하는 decorator
#     def get_tracking_param(cls, shortened_url_id):
#         return cls.objects.filter(shortened_url_id=shortened_url_id).values_list("params", flat=True)
# #         #values_list(*fields, flat=Falst, named=False)는 values()와 유사하나, values()가 dictionary를 반환하는데 반해, tuple을
# #         #반환함.


