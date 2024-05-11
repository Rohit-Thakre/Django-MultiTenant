from django.contrib import admin

# Register your models here.
from base.models import College, Student

admin.site.register(College)
admin.site.register(Student)