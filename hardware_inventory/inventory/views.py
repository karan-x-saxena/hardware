from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import Entry, Hardware, Machine,Section,Wing 
import datetime

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('home')
        messages.info(request,"enter correct username or password!")
    return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('login')

def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    return redirect('login')

def type_of_machine(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            machine = request.POST['machine']
            if machine == "":
                messages.info(request,"pls complete this field!")
                return redirect('machine')
            machine = machine.lower()
            if Machine.objects.filter(machine=machine).exists():
                messages.info(request,"this machine already exist!")
                return redirect('machine')
            Machine.objects.create(machine=machine).save
            redirect('machine')
        return render(request,'machine.html')
    return redirect('login')

def wing(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            wing = request.POST['wing']
            if wing == "":
                messages.info(request,"pls complete this field!")
                return redirect('wing')
            wing = wing.lower()
            if Wing.objects.filter(wing=wing).exists():
                messages.info(request,"this wing already exists!")
                return redirect('wing')
            Wing.objects.create(wing=wing).save()
            return redirect('wing')
        return render(request,'wing.html')
    return redirect('login')

def section_master(request):
    if request.user.is_authenticated:
        wing = Wing.objects.all().order_by('wing')
        if request.method == 'POST':
            section = request.POST['section']
            roomNO = request.POST['roomNO']
            newwing = request.POST['newwing']
            if section == "" or roomNO == "" or newwing == "select wing":
                messages.info(request,"pls complete all field!")
                return redirect('section')
            if roomNO.isdigit() == False:
                messages.info(request,"digits are allowed in room No.!")
                return redirect('section')
            section = section.lower()
            if Section.objects.filter(section=section).exists():
                messages.info(request,"this section already exists!")
                return redirect('section')
            Section.objects.create(section=section,roomNO=roomNO,wing=newwing).save()
            return redirect('section')
        return render(request,'section.html',{'wings':wing})
    return redirect('login')

def hardware(request):
    if request.user.is_authenticated:
        machinee = Machine.objects.all().order_by('machine')
        if request.method == 'POST':
            name = request.POST['machinename']
            number = request.POST['machineno']
            ids = request.POST['machineid']
            purchase = request.POST['purchase']
            cost = request.POST['cost']
            registerNo = request.POST['stockregister']
            specification = request.POST['Specifications']
            warrenty = request.POST['warrenty']
            year = request.POST['year']
            if number == "" or ids == "" or purchase == "" or cost == "" or registerNo == "" or specification == "" or year == "":
                messages.info(request,"pls complete all field!")
                return redirect('hardware')
            if cost.isnumeric() == False or registerNo.isnumeric() is False or year.isnumeric() == False:
                messages.info(request,"pls fill numeric data in Cost or Stock register pg No or Warenty time period feild!")
                return redirect('hardware')
            if (warrenty == "AMC" and year != '0') or (warrenty == "Sale warrenty" and year == '0') or (warrenty == 'None' and year != '0'):
                messages.info(request,"invalid entry in Warenty time period feild!")
                return redirect('hardware')
            if Hardware.objects.filter(machine_no=number).exists() or Hardware.objects.filter(U_id=ids).exists():
                messages.info(request,"Entry already exists!")
                return redirect('hardware')
            purchase_date = datetime.date(int(purchase[0:4]),int(purchase[5:7]),int(purchase[8:10]))
            new = Hardware.objects.create(machine_type=name,machine_no=number,U_id=ids,specification=specification,purchase_data=purchase_date,cost=cost,stock_register=registerNo,war_amc=warrenty,warrenty=year)
            new.save()
        return render(request,'hardware.html',{'machines':machinee})
    return redirect('login')

def entry_section(request):
    if request.user.is_authenticated:
        sections = Section.objects.all().order_by('section')
        if request.method == 'POST':
            username = request.POST['username']
            machine_id = request.POST['U_id']
            section_name = request.POST['sectionname']
            date = request.POST['date']
            print(username,machine_id,date,section_name)
            if machine_id == ""or date == "" or section_name=="nothing":
                messages.info(request,"pls complete all field!")
                return redirect('entry_sec')
            if Hardware.objects.filter(U_id= machine_id).exists():
                if Entry.objects.filter(machine_id=machine_id,status=False).exists():
                    old = Entry.objects.get(machine_id=machine_id,status=False)
                    old.status = True
                    old.save()
                wing = Section.objects.get(section=section_name)
                date = datetime.date(int(date[0:4]),int(date[5:7]),int(date[8:10]))
                entry = Entry.objects.create(machine_id=machine_id,sec_emp="sec",section_name=section_name,employee_name="Null",employee_id="Null",issue_date=date,username=username,wing=wing.wing)
                entry.save()
            else:
                messages.info(request,"machine Id not registered!")
                return redirect('entry_sec')
        return render(request,'entry_s.html',{'sections':sections})
    return redirect('login')

def entry_employee(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            e_name = request.POST['employeename']
            e_id = request.POST['employeeid']
            machine_id = request.POST['U_id']
            date = request.POST['date']
            if Hardware.objects.filter(U_id=machine_id).exists():
                if Entry.objects.filter(machine_id=machine_id,status=False).exists():
                    old = Entry.objects.get(machine_id=machine_id,status=False)
                    old.status = True
                    old.save()
                if e_name == "" or e_id =="" or date == "":
                    messages.info(request,"pls complete all field!")
                    return redirect('entry_emp')
                date = datetime.date(int(date[0:4]),int(date[5:7]),int(date[8:10]))
                entry = Entry.objects.create(machine_id=machine_id,sec_emp="emp",section_name="Null",employee_name=e_name,employee_id=e_id,issue_date=date,username=username,wing="NULL")
                entry.save()
            else:
                messages.info(request,"machine Id not registered!")
                return redirect('entry_emp')
        return render(request,'entry_e.html')
    return redirect('login')

def report(request):
    if request.user.is_authenticated:
        hardware = Hardware.objects.all().order_by('-id')
        return render(request,'datatable.html',{'hardwares':hardware})
    return redirect('login')

def entry_report(request):
    if request.user.is_authenticated:
        entry = Entry.objects.filter(sec_emp='emp').order_by('-id')
        data = {}
        j = 0
        for i in entry:
            hard = Hardware.objects.get(U_id=i.machine_id)
            data.update({str(j):[hard.machine_type,hard.specification,i]})
            j = j+1
        return render(request,'entry_table.html',{'datas':data})
    return redirect('login')

def section_report(request):
    if request.user.is_authenticated:
        entry = Entry.objects.filter(sec_emp='sec').order_by('-id')
        data = {}
        j = 0
        for i in entry:
            hard = Hardware.objects.get(U_id=i.machine_id)
            data.update({str(j):[hard.machine_type,hard.specification,i]})
            j = j+1
        return render(request,'section_table.html',{'datas':data})
    return redirect('login')
#Create your views here.
