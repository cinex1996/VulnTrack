from django.contrib import admin

from vulnerabilities.models import Vulnerability, Comment

# Register your models here.
admin.site.register(Vulnerability)
admin.site.register(Comment)