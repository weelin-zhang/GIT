#coding=utf-8
'''
Created on 2016年12月22日

@author: ZWJ
'''
from django import forms
#from logging import PlaceHolder

class RegisterUserForm(forms.Form):
    username = forms.CharField(min_length=6,widget=forms.TextInput({ "placeholder": "username"}))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "password"}),min_length=6)
    email = forms.EmailField(widget=forms.EmailInput({ "placeholder": "xxxx@ihangmei.com"}))
    
class LoginForm(forms.Form):
    username = forms.CharField(min_length=6,error_messages={'required':('用户名不能为空'),'invalid':('用户名格式不正确..')},widget=forms.TextInput({ "placeholder": "username"}))
    password = forms.CharField(widget=forms.PasswordInput({ "placeholder": "password"}))
    
