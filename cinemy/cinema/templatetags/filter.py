from django import template

register = template.Library()


@register.filter(name="in_list")
def in_list(value, list):
    return True if value in list else False


@register.filter(name="add_str")
def add_str(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter(name="format_time")
def format_time(input):
    input = int(input)
    return str(input // 60) + "h:" + str(input % 60) + "m"


@register.filter(name="get_url")
def get_url(input):
    return "https://www.youtube.com/embed/" + input.split("=")[-1]
