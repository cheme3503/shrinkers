from django import template
from django.utils.html import mark_safe

from datetime import time, datetime, date, timedelta

register = template.Library()  #custom tag를 사용하기 위해서는 template library 에 등록 하여야 함.

@register.filter(name="email_ma")  #custom filter 추가를 위한 데코레이터
def email_masker(value):
    email_split = value.split("@")

    return f"{email_split[0]}@*****.***"

@register.simple_tag(name="test_tags", takes_context=True) #custom tag를 template system으로 전달하기 위한 helper function
def test_tags(context):
    for c in context:
        print(c)
    tag_html = "<span class='badge badge-primary'>테스트 태그</span>"

    return mark_safe(tag_html) #simple_tags 는 output을 conditional_escape()을 통해 전달하는데, 추가적인 escaping을 원하지 않을때 사용