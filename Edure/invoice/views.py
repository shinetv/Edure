from django.core import paginator
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from . models import *
import easygui
from django.db.models import Sum
from Edure.utils import render_to_pdf
import pandas as pd
from django.core.paginator import Paginator
import datetime
from django.conf import settings 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import logout as log
# Create your views here.

def login(request):
    if request.method == "POST":
        name= request.POST['name']
        Password = request.POST['Password']
        Super = Admins.objects.filter(
            name=name, Password=Password, Std_Type="Superadmin")
        Admin = Admins.objects.filter(
            name=name, Password=Password, Std_Type="Admin")
       
        # admin = Tbl_Registration.objects.filter(Adm_UserName=username, Adm_Password=password,Adm_Type="Admin")
        if Super:
            for x in Super:
                request.session['id'] = x.id
                request.session['name'] = x.name
                request.session['Std_Type'] = x.Std_Type
                request.session['Password'] = x.Password
                print("________________________", request.session['id'])
                return HttpResponseRedirect('/detail/')
        elif Admin:
            for x in Admin:
                request.session['id'] = x.id
                request.session['name'] = x.name
                request.session['Std_Type'] = x.Std_Type
                request.session['Password'] = x.Password
                print("________________________", request.session['id'])
                return HttpResponseRedirect('/detail/')
        else:
            return render(request, 'log.html', {'msg': 'Invalid login credentials.!'})
    else:
        return render(request,'log.html')
    

def detail(request):
    
    aa = Stud_reg.objects.all()
    x             = datetime.datetime.now()
    date          =x.strftime("%m/%d/%Y")    
    length = len(aa)
    print("_________________", length)

    idd = 10000
    aa = str(idd).zfill(6)
    studid = "ed"+aa
    if request.method=="POST":
            if Stud_reg.objects.filter(Stud_mail=request.POST['Stud_mail']):
                easygui.msgbox("This Email already Exits")
            elif Stud_reg.objects.filter(Stud_number=request.POST['Stud_number']):
                 easygui.msgbox("This Phone number already Exists")    
            elif Stud_reg.objects.filter(Stud_number=request.POST['Stud_name']):
                 easygui.msgbox("This Student Name already Exists")  
                         
            else:
                
                stud_data=Stud_reg()
                stud_data.Stud_name=request.POST['Stud_name']
                stud_data.Stud_mail=request.POST['Stud_mail']
                stud_data.Stud_course=request.POST['Stud_course']
                stud_data.Stud_number=request.POST['Stud_number']
                stud_data.Stud_balance=request.POST['Stud_balance']
                stud_data.Stud_paid=request.POST['Stud_paid']
                stud_data.Stud_address=request.POST['Stud_address']
                stud_data.Course_amount=request.POST['Course_amount']
                stud_data.Join_date=date
                if len(request.FILES)!=0:
                    stud_data.Stud_image=request.FILES['Stud_image']
                stud_data.End_date=request.POST['End_date']
                stud_data.Stud_IDD=studid
                subject = 'welcome to Edure world'
            # message = f'Hi {name}, thank you for registering.your password is:{newpassword}'
            # message = f'Hi ,Welcome to Edvest \nyour Edvest Login Credentials is .\n User name :</b>{user}Password :{psw}\nand your Edvest ID is {uid}Don\'t share with anyone.'
                message=render_to_string('email_message.html', {
                            'user': stud_data.Stud_name,
                            'psw': stud_data.Stud_course,
                            'uid': stud_data.Stud_paid,
                            'pdate':stud_data.End_date,
                            'balance':stud_data.Stud_balance
                        })            
                email_from = settings.EMAIL_HOST_USER 
                recipient_list = [stud_data.Stud_mail, ] 
                send_mail( subject, message, email_from, recipient_list )
                stud_data.save()
               
                return redirect(details)
    
   
    return render(request,'details.html')    


def details(request):
    SessionId=request.session['id']
    stud=Stud_reg.objects.all()
    stud_count=Stud_reg.objects.all().count()
    total=Stud_reg.objects.all().aggregate(TOTAL = Sum('Stud_paid'))['TOTAL']
    paginator=Paginator(stud,5)
    page_number=request.GET.get('page')
    studfinal=paginator.get_page(page_number)
    
    return render(request,'All_detail.html',{'stud':studfinal,'stud_count':stud_count,'total':total})    



def DownloadCV(request):
    i = request.GET['id']
    stud=Stud_reg.objects.all().filter(id=i)
    pdf = render_to_pdf('invoice.html',{'stud':stud})
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=invoice.pdf'
    return response

def downloadCSV(request):
   
    data = Stud_reg.objects.all().values('Stud_name','Stud_mail','Stud_number','Stud_address','Join_date','Stud_course','Course_amount','Stud_paid','Stud_balance','End_date')
    data_frame = pd.DataFrame(list(data), index=None)
    csv = data_frame.to_csv(header=[ "Name", "Mail Id","Phone Number","Address","Join Date","Course Opt","Course Fee","Student Paid","Balance Amount","Paid Date"], index=True)
    response = HttpResponse(csv, content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="Receipientlist"'+str(datetime.datetime.now())+'".csv"'
    return response

def update(request,id):
    stud=Stud_reg.objects.get(id=id)
    if request.method=="POST":
        Stud_course=request.POST['Stud_course']
        Stud_balance=request.POST['Stud_balance']
        Stud_paid=request.POST['Stud_paid']
        Course_amount=request.POST['Course_amount']
        End_date=request.POST['End_date']
        stu=Stud_reg.objects.all().filter(id=id).update(Stud_course=Stud_course,Stud_balance=Stud_balance,
                                                        Stud_paid=Stud_paid,Course_amount=Course_amount,End_date=End_date  )
        return render(request,'update.html',{'msg': 'Data Updated.!'})
    else:
        return render(request,'update.html',{'stud':stud})

def logout(request):
    log(request)
    return render(request,'log.html')
