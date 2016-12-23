#coding=utf8
from django.contrib import admin
from appgit import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=('username','email')#在admin中现实的内容，不仅仅显示一个对象
    
    #search_fields = ('', '')#添加搜索功能
    
    #list_filter = ('', '')#添加快速过滤
class DepartmentAdmin(admin.ModelAdmin):
    list_display=('dpname',)
    
    
admin.site.register(models.UserInfo,UserAdmin)
admin.site.register(models.Department,DepartmentAdmin)