import datetime
from django import template

register = template.Library()


@register.filter(name="format_time")
def format_time(input):
    input = int(input)
    return str(input // 60) + "h:" + str(input % 60) + "m"
