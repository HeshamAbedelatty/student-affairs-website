from asyncio import queues
from turtle import mode
from unicodedata import name
from django.shortcuts import render
from .models import studentdataa, studentaffairsadmin,activeuser
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages,auth
from ssl import AlertDescription
from datetime import datetime
from django.shortcuts import  render, redirect
from django.http import HttpRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.template import loader
from django.urls import reverse
def welcomepage(request):
    return render(request,'welcomepage.html')
def loginpage(request):
    if request.method == 'POST':
        usernamee = request.POST['username'] 
        passworde =request.POST['pass']
        if studentaffairsadmin.objects.filter(username=usernamee).exists():
            ll=studentaffairsadmin.objects.get(username=usernamee)
            if ll.password == passworde:
                if activeuser.objects.filter(status='inactive',username=usernamee).exists():
                    temp=activeuser.objects.get(status='inactive',username=usernamee)
                    temp.status='active'
                    temp.save(update_fields=['status'])
                    return redirect('../homepage')
                
                return redirect('../homepage')
            else: 
              messages.error(request,"password is incorrect. please try again")
              return redirect('../loginpage')  
        else:
          messages.error(request,"username is incorrect. please try again")
          return redirect('../loginpage')
    return render(request, 'loginpage.html')
def signout(request):
    temp=activeuser.objects.get(status='active')
    temp.status='inactive'
    temp.save(update_fields=['status'])
    return redirect('../loginpage')  
def forgetpasswordpage(request):
    if request.method == 'POST':
      subject="Recover Your Email in studentaffairs project"
      eemail = request.POST['recoverdemail']
      if studentaffairsadmin.objects.filter(email=eemail).exists():
            recover=studentaffairsadmin.objects.get(email=eemail)
            message='your username is %s and password is %s'%(recover.username,recover.password)
            email=EmailMessage(subject,message,to=[eemail])
            email.send()
            messages.success(request,"open your mail to get the username and password")
            return redirect('../loginpage')     
      else:
          messages.error(request,"email is not correct please try again")
          return redirect('../forgetpasswordpage')
    return render(request, 'forgetpasswordpage.html')
def registerpage (request):
    if request.method == 'POST':
        # nationalnume =request.POST['national']
        nationalnume = request.data.get('national')
        namee= request.POST['adminName']
        phonee=request.POST['PHONEE']
        emaile=request.POST['emaila']
        dateofbirthe=request.POST['adminDob']
        usernamee=request.POST['adminusername']
        passworde=request.POST['adminpass']
        if studentaffairsadmin.objects.filter(username = usernamee).exists():
            messages.info(request, 'Sorry. This username is taken please try again')
            return render(request, 'registerpage.html')
        if studentaffairsadmin.objects.filter(nationalnum = nationalnume).exists():
            messages.info(request, 'Sorry. This national number is taken please try again')
            return render(request, 'registerpage.html')
        if studentaffairsadmin.objects.filter(phone = phonee).exists():
            messages.info(request, 'Sorry. This phone is taken please try again')
            return render(request, 'registerpage.html')
        if studentaffairsadmin.objects.filter(email = emaile).exists():
            messages.info(request, 'Sorry. This email is taken please try again')
            return render(request, 'registerpage.html')
        if   len(nationalnume) !=14 :
            messages.error(request, 'Sorry. national number length should be 14 ')
            return render(request, 'registerpage.html')
        if len(passworde)<8:
            messages.error(request, 'Sorry. password length should be 8 or more ')
            return render(request, 'registerpage.html')
        else:    
            p = studentaffairsadmin(
                    nationalnum = nationalnume,
                    name= namee,   
                    phone=phonee,
                    email=emaile,
                    username=usernamee,
                    password=passworde,  
                    dateofbirth=dateofbirthe,    
             )
            p.save()
            i=activeuser(status='inactive',username=usernamee)
            i.save()
            return redirect('../loginpage')
    
    return render(request,'registerpage.html')

def homepage(request):
    if activeuser.objects.filter(status='active').exists():
        return render(request,'homepage.html')
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')





     
    

def addstudent(request):
    if activeuser.objects.filter(status='active').exists():
        if request.method == 'POST':
            namea =request.POST['studname']
            ida= request.POST['studid']
            phonea=request.POST['studphone']
            emaila=request.POST['studemail']
            dateofbirtha=request.POST['dobb']
            nationalnuma=request.POST['studnat']
            gpaa=request.POST['studgpa']
            gendera=request.POST['gender']
            levela=request.POST['level']
            statusa=request.POST['status']
            departmenta=request.POST['department']
            if studentdataa.objects.filter(id = ida).exists():
                messages.error(request, 'Sorry. This id is taken please try again')
                return render(request, 'addstudent.html')
            if studentdataa.objects.filter(nationalnum = nationalnuma).exists():
                messages.error(request, 'Sorry. This national number is taken please try again')
                return render(request, 'addstudent.html')
            if studentdataa.objects.filter(phone = phonea).exists():
                messages.error(request, 'Sorry. This phone is taken please try again')
                return render(request, 'addstudent.html')
            if studentdataa.objects.filter(email = emaila).exists():
                messages.error(request, 'Sorry. This email is taken please try again')
                return render(request, 'addstudent.html')
            if   int(levela) <=2 and departmenta!='None':
                messages.error(request, 'Sorry. you can assign department only to students with level 3 or 4')
                return render(request, 'addstudent.html')
            if   len(nationalnuma) !=14 :
                messages.error(request, 'Sorry. national number length should be 14 ')
                return render(request, 'addstudent.html')
            if len(ida)<7:
                messages.error(request, 'Sorry. student id length should be 7 or more ')
                return render(request, 'registerpage.html')
            q = studentdataa(
                        id=ida,
                        nationalnum = nationalnuma,
                        name= namea,
                        dateofbirth=dateofbirtha,    
                        phone=phonea,
                        email=emaila,
                        gpa=gpaa,
                        level=levela,
                        department=departmenta,
                        status=statusa,  
                        gender=gendera 
                        )
            q.save()
            messages.success(request, 'New Student is added successfully')
            return redirect('../addstudent')
        return render(request,'addstudent.html')
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')





def active(request):
    if activeuser.objects.filter(status='active').exists():
        ACTstuds = studentdataa.objects.filter(status='Active').order_by('id')
        template = loader.get_template('active.html')
        context = {
            'actstud': ACTstuds
        }
        return HttpResponse(template.render(context, request))     
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')

def inactive(request):
    if activeuser.objects.filter(status='active').exists():
        INACTstuds = studentdataa.objects.filter(status='Inactive').order_by('id')
        template = loader.get_template('inactive.html')
        context = {
            'inactstud': INACTstuds
        }
        return HttpResponse(template.render(context, request))     
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')
    
def showstudent(request):
    if activeuser.objects.filter(status='active').exists():
        allstud =  studentdataa.objects.all().order_by('id')
        template = loader.get_template('showstudent.html')
        context = {
            'allstu': allstud
        }
        return HttpResponse(template.render(context, request))     
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')
    
def delstud(request,z):
    if activeuser.objects.filter(status='active').exists():
        if studentdataa.objects.filter(id=z).exists():
            tem=studentdataa.objects.filter(id=z).delete()
        studs = studentdataa.objects.all().order_by('id')
        template = loader.get_template('deletestudent.html')
        context = {
            'stud': studs
        }
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')

def deletestudent(request):
    if activeuser.objects.filter(status='active').exists():
        studs = studentdataa.objects.all().order_by('id')
        template = loader.get_template('deletestudent.html')
        context = {
            'stud': studs
        }
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')


def search(request):
    if activeuser.objects.filter(status='active').exists():
        return render(request,'search.html')
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')


def searchdown(request):
    if activeuser.objects.filter(status='active').exists():
        nn=request.GET['studd']
        ss=request.GET['stat']
        if ss=='All':
            if (studentdataa.objects.filter(Q(name__contains=nn)|Q(id__contains=nn))).exists():
                tem=studentdataa.objects.filter(Q(name__contains=nn)|Q(id__contains=nn)).order_by('id')
                template = loader.get_template('searchdown.html')
                context = {
                'hh': tem
                }
                return HttpResponse(template.render(context, request))
            return render(request,'searchdown.html')
        else:
            if (studentdataa.objects.filter(Q(name__contains=nn)|Q(id__contains=nn))& studentdataa.objects.filter(status=ss)).exists():
                tem=studentdataa.objects.filter(Q(name__contains=nn)|Q(id__contains=nn))& studentdataa.objects.filter(status=ss).order_by('id')
                tem.distinct()
                template = loader.get_template('searchdown.html')
                context = {
                'hh': tem
                }
                return HttpResponse(template.render(context, request))
            return render(request,'searchdown.html')
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')


def delstud(request,z):
    if activeuser.objects.filter(status='active').exists():
        if studentdataa.objects.filter(id=z).exists():
            tem=studentdataa.objects.filter(id=z).delete()
        studs = studentdataa.objects.all().order_by('id')
        template = loader.get_template('deletestudent.html')
        context = {
            'stud': studs
        }
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')

def deletestudent(request):
    if activeuser.objects.filter(status='active').exists():
        studs = studentdataa.objects.all().order_by('id')
        template = loader.get_template('deletestudent.html')
        context = {
            'stud': studs
        }
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')


def departmentassign(request,n):
    if activeuser.objects.filter(status='active').exists():
        if studentdataa.objects.filter(id=n).exists():
            tempp=studentdataa.objects.get(id=n)
            template = loader.get_template('departmentassign.html')
            context = {
            'name': tempp.name,
            'id':tempp.id,
            'dept':tempp.department
            }
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')

def changedept(request,n):
    if activeuser.objects.filter(status='active').exists():
        a=request.GET['deptt']
        b=request.GET['tt']
        if studentdataa.objects.filter(id=b).exists():
            tempp=studentdataa.objects.get(id=b)
            template = loader.get_template('departmentassign.html')
            context = {
                'name': tempp.name,
                'id':tempp.id,
                'dept':tempp.department
                }
            if int(tempp.level)>=3:
                tempp.department=a
                tempp.save(update_fields=['department'])
                template = loader.get_template('departmentassign.html')
                context = {
                    'name': tempp.name,
                    'id':tempp.id,
                    'dept':tempp.department
                    }
                messages.success(request,"Successfull")
                return HttpResponse(template.render(context, request))               
            else:
                messages.error(request,"Sorry you can only assign a department to students level is 3 or more")
                return HttpResponse(template.render(context, request)) 
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')




def adminprofilepage(request):
    if activeuser.objects.filter(status='active').exists():
        temp=activeuser.objects.get(status='active')
        res=studentaffairsadmin.objects.get(username=temp.username)
        template = loader.get_template('adminprofilepage.html')
        context={
        'Name':res.name,
        'BirthDate':res.dateofbirth,
        'Phone':res.phone,
        'Email':res.email,
        'Username':res.username,
        'Password':res.password,
        'NationalNumber':res.nationalnum,}
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')



def updateadmindata(request):
    if activeuser.objects.filter(status='active').exists():
        n2=request.GET['national1']
        if studentaffairsadmin.objects.filter(nationalnum = n2).exists():
            t=studentaffairsadmin.objects.get(nationalnum = n2)
            n=t.name
            d=t.dateofbirth
            p=t.phone
            e=t.email
            u=t.username
            p2=t.password
            if t.name!=request.GET['adminName1']:
                n=request.GET['adminName1']
            if t.dateofbirth!=request.GET['adminDob1']:
                d=request.GET['adminDob1']
            if t.phone!=request.GET['PHONEE1']:
                p=request.GET['PHONEE1']
                if studentaffairsadmin.objects.filter(phone = p).exists():
                    messages.info(request, 'Sorry. This phone is taken please try again')
                    return redirect('../adminprofilepage')
            if t.email!=request.GET['emaila1']:
                e=request.GET['emaila1']
                if studentaffairsadmin.objects.filter(email = e).exists():
                    messages.info(request, 'Sorry. This email is taken please try again')
                    return redirect('../adminprofilepage')
            if t.username!=request.GET['adminusername1']:
                u=request.GET['adminusername1']
                if studentaffairsadmin.objects.filter(username = u).exists():
                    messages.info(request, 'Sorry. This username is taken please try again')
                    return redirect('../adminprofilepage')
            if t.password!=request.GET['adminpass1']:
                p2=request.GET['adminpass1']
                if len(p2)<8:
                    messages.error(request, 'Sorry. password length should be 8 or more ')
                    return redirect('../adminprofilepage')
        if studentaffairsadmin.objects.filter(nationalnum=n2).exists():
            temp=studentaffairsadmin.objects.get(nationalnum=n2)

            oo=activeuser.objects.filter(username=temp.username).delete()
            


            i=activeuser(status='active',username=u)
            i.save()
            temp.name=n
            d=datetime.strptime(d,"%b. %d, %Y").date()

            temp.dateofbirth=d
            temp.phone=p
            temp.email=e
            temp.username=u
            temp.password=p2
            temp.save(update_fields=['name','dateofbirth','phone','email','username','password'])
            template = loader.get_template('adminprofilepage.html')
            context={
                'Name':temp.name,
                'BirthDate':temp.dateofbirth,
                'Phone':temp.phone,
                'Email':temp.email,
                'Username':temp.username,
                'Password':temp.password,
                'NationalNumber':temp.nationalnum,}
        return HttpResponse(template.render(context, request))
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')

def update2(request):
    if activeuser.objects.filter(status='active').exists():
        temp=request.GET.get('StudentNUM',None)
        if studentdataa.objects.filter(id=temp).exists():
            tempp=studentdataa.objects.get(id=temp)
            template = loader.get_template('update2.html')
            context = {
            'id': tempp.id,
            'name':tempp.name,
            'dateofbirth':tempp.dateofbirth,
            'nationalnum':tempp.nationalnum,
            'gpa':tempp.gpa,
            'gender':tempp.gender,
            'level':tempp.level,
            'status':tempp.status,
            'department':tempp.department,
            'email':tempp.email,
            'phone':tempp.phone
            }
            return HttpResponse(template.render(context, request))
        return render (request,'update2.html',{'StudentNUM':context})
    messages.error(request,"Sorry you must login first")
    return redirect('../loginpage')




def studupdate(request):
        studid=request.GET.get('studentid',None)
        if studentdataa.objects.filter(id = studid).exists():
            rest=studentdataa.objects.get(id =studid )      
            stname=rest.name
            stnational=request.GET.get('studentnationalnum',None)
            stdob=rest.dateofbirth
            stphone=request.GET['studentphone']
            stemail=request.GET.get('studentemail',None)
            stgpa=rest.gpa
            stlevel=rest.level
            stdept=rest.department
            ststatus=rest.status
            stgender=rest.gender
            if rest.name!=request.GET.get('studentname',None):
                stname=request.GET.get('studentname',None)

            if rest.nationalnum!=stnational:
                if studentdataa.objects.filter(nationalnum = stnational).exists():
                    messages.error(request, 'Sorry. This national num is taken please try again') 
                    return render (request,'update2.html',{'StudentNUM':studid})     
                rest.nationalnum=stnational

            if rest.phone!=stphone:
                if studentdataa.objects.filter(phone = stphone).exists():
                    messages.error(request, 'Sorry. This phone is taken please try again')
                    return render (request,'update2.html',{'StudentNUM':studid})     
                rest.phone=stphone

            if rest.email!=stemail:
                if studentdataa.objects.filter(email = stemail).exists():
                    messages.error(request, 'Sorry. This email is taken please try again')
                    return render (request,'update2.html',{'StudentNUM':studid})     
                rest.email=stemail
  

            if rest.dateofbirth!=request.GET.get('studentdateofbirth',None):
                stdob=request.GET.get('studentdateofbirth',None)

            if rest.gpa!=request.GET.get('studentgpa',None):
                stgpa=request.GET.get('studentgpa',None)

            if rest.level!=request.GET.get('level',None):
                stlevel=request.GET.get('level',None)

            if rest.department!=request.GET.get('studentdepartment',None):
                stdept=request.GET.get('studentdepartment',None)

            if rest.status!=request.GET.get('status',None):
                ststatus=request.GET.get('status',None)

            if rest.gender!=request.GET.get('gender',None):
                stgender=request.GET.get('gender',None)

            

            if len(stnational)!=14:
                messages.error(request, 'Sorry.  national num length should be 14')
                return render (request,'update2.html',{'StudentNUM':rest.id})

                
                
            if len(stphone)>15:
                messages.error(request, 'Sorry.  phone length should be less than or equal 15')
                return render (request,'update2.html',{'StudentNUM':rest.id})
                
 
                
            rest.name=stname
            
            stdob=datetime.strptime(stdob,"%b. %d, %Y").date()
            rest.dateofbirth=stdob
            
            
            rest.gpa=stgpa
            rest.level=stlevel
            rest.department=stdept
            rest.status=ststatus
            rest.gender=stgender
            rest.save(update_fields=['name','nationalnum','dateofbirth','phone','email','gpa','level','department','status','gender'])
            template2 = loader.get_template('update2.html')
            context2 = {
            'id': rest.id,
            'name':rest.name,
            'dateofbirth':rest.dateofbirth,
            'nationalnum':rest.nationalnum,
            'gpa':rest.gpa,
            'gender':rest.gender,
            'level':rest.level,
            'status':rest.status,
            'department':rest.department,
            'email':rest.email,
            'phone':rest.phone
            }
            messages.success(request, 'Successfull') 
            return HttpResponse(template2.render(context2, request))
        return redirect('../update2'+'?StudentNUM=rest.id')