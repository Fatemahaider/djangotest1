from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
#from django.contrib.auth import authenticate
from django.contrib import auth
from django.db import connection

#from django.db import connections
#cursor = connections.cursor()


# Create your views here.

def home (request):
    context = {
        'title':'a'

    }
    

    return render(request,'base.html',context) 

class homec (TemplateView):

    
    template_name = 'base.html'

class Register(View):
    def get(self,request):
        return render(request,'register.html')

    def post (self,request):

        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        emailval = request.POST['email']
        pwd = request.POST['password']
        password = str(pwd)
        cpwd = request.POST['cpassword']
        

        content = {
            'formval': request.POST
        }

        if not password == cpwd :
            messages.error(request,"Password didn't match ")
            return render (request,'register.html',content)
        if not str(username).isalnum() :
            messages.error(request,"Invalid Username ")
            return render(request,'register.html',content)
        if not validate_email(emailval) :
            messages.error(request,"Invalid Email ")
            return render(request,'register.html',content)
        
        if  not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=emailval).exists():
                if len(password) < 6:
                    messages.error(request,"password Too short min 6 ")
                    return render(request,'register.html',content)
                user = User.objects.create_user(username=username,email=emailval,first_name=fname,last_name=lname)
                user.set_password(password)
                user.is_active=True
                user.save()
                messages.success(request,"Account Created successfully")
                '''email_sub = "Activate Your Account"
                email_body ="Test Body"
                
                email = EmailMessage(
                email_sub,
                email_body,
                'noreply@semycolon.com',
                [emailval],
                )       
                
                email.send(fail_silently=False)
                messages.info(request,"Check Mail for Activation")    
'''
                return redirect('login')
        
        return render(request,'register.html',content)    

class LoginView(View):
    def get (self,request):

        content = {
            'formval': request.body
        }
        return render(request, 'login.html', content)

    def post (self,request):

        
        content = {
            'formval': request.POST
        }



        uname = request.POST['username']
        pwd = request.POST['password']
        
        if uname and pwd :
            user = auth.authenticate(username=uname , password=pwd)
            # import pdb
            # pdb.set_trace()
            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,f'Welcome {user}')
                    return redirect('user_expense')
            messages.error(request,'Invalid Credentials, try again' )
            return render(request,'login.html',content)    
            
        return render(request,'login.html',content)    

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.info(request,f"You have been logged out")
        return redirect('login')

class Unamevalid(View):
    
    def post (self ,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum() :
            return JsonResponse({'Username_error' :'Username should only contain alphanumeric characters'},status = 400)         
        if User.objects.filter(username=username).exists():
            return JsonResponse({'Username_error': 'Username Already Exist'},status = 409)
        return JsonResponse({'Username_valid':True})    
        
        '''if str(username).isalnum():
             cursor.execute("SELECT * FROM `auth_user` WHERE username = %s",(username,))
             a = cursor.fetchall()
             if a :
                return JsonResponse({'username': 'Username Already Exist'},status = 400)
        '''

class Emailvalid(View):
    
    def post (self ,request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email) :
            return JsonResponse({'email_error' :'invalid email'},status = 400)         
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email Already Exist'},status = 409)
        return JsonResponse({'email_valid':True})    

