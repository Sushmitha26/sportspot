from django.shortcuts import render, redirect 
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.
def signup(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        usn=request.POST.get('usn')
        phone=request.POST.get('phone')
        branch=request.POST.get('branch')
        year=request.POST.get('year')
        gender=request.POST.get('gender')
        password =make_password(request.POST.get('password'))
    
        try:
            Student.objects.get(usn=usn)
            messages.info(request,'The usn you entered has already been taken. Please enter another usn.')
            return render(request, 'dashboard/signup.html')
        
        except:
            try:
                Student.objects.get(phone=phone)
                messages.info(request,'The phone number you entered has already been taken. Please enter another one.')
                return render(request, 'dashboard/signup.html')
                
            except:
                try:
                    Student.objects.get(email=email)
                    messages.info(request,'The email you entered has already been taken. Please enter another one.')
                    return render(request, 'dashboard/signup.html')
                
                except:
                    data = Student(name=name,email=email,usn=usn,phone=phone,branch=branch,year=year,gender=gender,password=password)
                    data.save()
                    print("User created")
                    return redirect("/")
            
    return render(request,'dashboard/signup.html')

def login(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user = Student.objects.get(email = email)
             
            if check_password(password,user.password):
                request.session['email'] = email
                return redirect('/dashboard/') 
            else:
                messages.info(request,'password does not match')
        except Student.DoesNotExist:
            messages.info(request,'Invalid email')
        
        return render(request, 'dashboard/login.html')

    return render(request, 'dashboard/login.html')

def dashboard(request):
    try:
        request.session['email']
        if request.method == 'POST':
            suggestion = request.POST.get('suggestion_text')
            data = Suggestions(suggestion=suggestion)
            data.save()
            return redirect("/dashboard/")
        return render(request, 'dashboard/dashboard.html') 
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')

def mentors(request):
    try:
        request.session['email']
        ments = Mentor.objects.all()
        context = {'ments' : ments, 'home_page': 'active'}
        return render(request, 'dashboard/mentor.html', context)
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')

def events(request):
    try:
        email=request.session['email']
        eves = Events.objects.all()
        student=Student.objects.get(email=email)
        context = {'eves':eves, 'usn':student.usn, 'name':student.name, 'home_page': 'active'}

        if request.method == 'POST':
            event_name=request.POST.get('event_name')
            event = Events.objects.get(event_name=event_name)
            try:
                Enrollment.objects.get(student=student,event=event) 
                messages.info(request,"You have already registered!!")
                return render(request, 'dashboard/events.html',context)
            except:
                all_events = list(Enrollment.objects.filter(student=student))
                for one_event in all_events:
                    if one_event.event.date==event.date:
                        messages.info(request,"You have enrolled for other event on the same day!!")
                        return render(request, 'dashboard/events.html',context)
                    
                data=Enrollment(student=student,event=event)
                data.save()
                messages.success(request,'You have successfully registered!!')
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')

    return render(request, 'dashboard/events.html',context)
    
def shortlisted(request):
    try:
        request.session['email']
        eves = Events.objects.all()
        mydict = {}
        for eve in eves:
            data = list(Enrollment.objects.filter(selected=True,event=eve))
            if len(data)!=0:
                mydict[eve]=data
            context = {'mydict':mydict,'home_page': 'active'}

        return render(request, 'dashboard/shortlisted.html',context)
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')

def gallery(request):
    try:
        request.session['email']
        gals = Gallery.objects.all()
        context = {'gals' : gals}
        return render(request, 'dashboard/gallery.html',context)
    except:
        messages.info(request,'You are not logged in!!')
        return redirect('/')

def logout(request):
    del request.session['email']
    return redirect('/')
    

