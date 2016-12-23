from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    department = models.ForeignKey('Department')
    idrsa = models.CharField(max_length=2500)
    idrsapub = models.CharField(max_length=2500)
    createtime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.username
    
class Department(models.Model):
    dpname = models.CharField(max_length=50)
    def __unicode__(self):
        return self.dpname