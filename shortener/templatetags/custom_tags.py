from django import template
from django.utils.safestring import mark_safe

from datetime import time, datetime, date, timedelta

register = template.Library()

@register.filter(name="email_ma")
def email_masker(value, arg=None):
    email_split = value.split("@")
    print(arg)
    return f"{email_split[0]}@*****.***" if arg %2 == 0 else value


@register.simple_tag(name="test_tags", takes_context=True)
def test_tags(context): # Page containing information in 'context'
    for c in context: # 'for' loop makes rendering slow
        i = 1
        print(c, " ", i)
        i += 1
    tag_html = "<span>test tag</span>"

    return mark_safe(tag_html) # this tag is trustworty.