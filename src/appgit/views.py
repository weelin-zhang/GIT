#coding=utf8
from django.shortcuts import render,redirect,HttpResponse
from appgit import models
import json,os,commands
from tool.SendMail import *
from appgit.forms import RegisterUserForm,LoginForm
# Create your views here.

#搞一个装饰器
def checkLogin(func):
    
    def wrapper(request,*args,**kwargs):
        if not request.session.get('is_login',None):
            print 'no logined'
            return redirect('/appgit/login')
        return func(request,*args,**kwargs)
    return wrapper

def register(request,*args,**kwargs):
    originform = RegisterUserForm()
    ret = {}
    departmentobjs = models.Department.objects.all()    
    ret['departments'] =  departmentobjs
    if request.method=='POST':
        #data = request.form
        checkform = RegisterUserForm(request.POST)#user,password,email
        if not checkform.is_valid():#为firefox,IE等sb准备
            ret['status'] = '密码，用户名长度大于6'
            ret['form'] = checkform
            return render(request, 'appgit/register.html',ret)
        result_form=checkform.clean()
        #就判断用户名是否存在
        user=result_form['username']
        if models.UserInfo.objects.filter(username=user).count():
            ret['status']='用户存在,change'
            ret['form'] = checkform
            return render(request, 'appgit/register.html',ret)
        
        departmentid = request.POST['department']
        
        #获取秘钥和公钥
        #cmd='rm /home/supsa/rsadir/id_rsa* > /dev/null;/usr/local/bin/expect /home/supsa/rsadir/expect.sh %s >/dev/null ;cat /home/supsa/rsadir/id_rsa.pub >>~/.ssh/authorized_keys'%(result_form['email'])
        #cmdresultcode = commands.getstatusoutput(cmd)[0]
        #if cmdresultcode:#执行失败
            #return HttpResponse('创建密钥失败..')
        
        #拿到私钥,公钥--linux
        #with open('/home/supsa/rsadir/id_rsa','rb') as f:
            #id_rsa = f.read()
        
        #with open('/home/supsa/rsadir/id_rsa.pub','rb') as f:
            #id_rsapub = f.read()   
        #拿到私钥,公钥--linux
        
        with open(r'D:\workspace\GIT\src\tool\id_rsa_w','rb') as f:
            id_rsa = f.read()
        print 'aaaaa:',id_rsa
        id_rsapub='''ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA4Q7mwu9nKsOpbNnonnxA9W+n8byhgBYq/OqWqVBZlW8fL417av8ThcBtK7GV1iODt0zSJVe0zTtUsKljJET6em9s09IzD5eags7rnWNQnWVhrXsaFH6Pxv3Vyj9vSRMoSVHjg9FFR7rT8jFFH8lUg+ZHL2q+Ue8KvgF3DLjD15uUXPItIzBan+qgOl3SA+jKIdZXFAuN1VbY1i04uC+sHRwZIE1K5xLR92WVxfLVRTE/Y6IUZW58lgGHzDBuQj6vFNCtSPe6Bfb5eM4ggmBDgXLkmQwj95vlWj5CClg7IU20Mvji4JHJ4MGWGcCzbJv6rPzIuXRYR4/jz+RXZfoQqQ== weimin@ihangmei.com'''
         
        departmentobj = models.Department.objects.filter(id=departmentid)[0]
        #print 'register info:',result_form['username'],result_form['email'],departmentobj.dpname
        #存入数据库
        try:
            
            #发送邮件--->
            mailto_list = result_form['email'].split()
            sub = u'git 私钥'
            attachment_path= [r'D:\workspace\GIT\src\tool\id_rsa_w',r'D:\workspace\GIT\src\tool\README.txt']
            #attachment_path= ['/home/supsa/rsadir/id_rsa','/home/supsa/rsadir/README.txt']
            if not send_mail_fujian(mailto_list,sub,attachment_path,mail_host,mail_user,mail_pass):
                return HttpResponse('发送失败')
            try:
                userobj = models.UserInfo.objects.create(username = result_form['username'],password=result_form['password'],email = result_form['email'],idrsapub=id_rsapub,idrsa=id_rsa,department=departmentobj)
                request.session['is_login'] = {'user':userobj.username,'status':True}
                return HttpResponse(u'<p>私钥和说明文件已经以附件的方式发送到邮箱%s,<a style="text-decoration:none" href="/appgit/logout/">退出登录</a></p>'%mailto_list[0])
            except:
                return HttpResponse(u'<p>数据库异常,<a style="text-decoration:none" href="/appgit/register/">重试</a></p>')
            return redirect('/appgit/index')
        except Exception as e:  
            print 'add user fail,',e
            ret['status']='请重新尝试...'
            ret['form'] = originform
            return render(request, 'appgit/register.html',ret) 
    ret['form'] = originform
    return render(request, 'appgit/register.html',ret)



def login(request,*args,**kwargs):
    ret={}
    if request.method=='POST':
        data = request.POST
        print data
        user = data['username']
        pwd = data['password']        
        if not models.UserInfo.objects.filter(username=user):
            ret['status']='用户不存在'
            return render(request, 'appgit/login.html',ret)
        loginobj = models.UserInfo.objects.get(username=user) 
        if user == loginobj.username and pwd == loginobj.password:
            ret['status']='login success'
            #session
            request.session['is_login'] = {'user':user,'status':True}
            return redirect('/appgit/index/')
        else:
            ret['status']='密码错误..'
            return render(request, 'appgit/login.html',ret) 
        print data
    
    return render(request, 'appgit/login.html',ret)


def index(request,*args,**kwargs):
    ret={}
    if request.session.get('is_login'):
        loginuser = request.session.get('is_login')['user']
        #拿到私钥
        if not models.UserInfo.objects.filter(username=loginuser):
            return redirect('/appgit/login/')
        useridrsa = models.UserInfo.objects.filter(username=loginuser)[0].idrsa.rstrip()
        ret['loginuser']=loginuser
        ret['idrsa']=useridrsa
        return render(request,'appgit/index.html',ret)
    return redirect('/appgit/login/')


@checkLogin     
def logout(request,*args,**kwargs):
    
    del request.session['is_login']
    
    return redirect('/appgit/login/')
