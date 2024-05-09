from django.contrib import admin
from . models import studentdataa, studentaffairsadmin, activeuser

# Register your models here.
admin.site.register(studentdataa)
admin.site.register(studentaffairsadmin)
admin.site.register(activeuser)