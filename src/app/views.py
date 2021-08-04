from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from .models import Manual
from Switches_Connecter import connecter
from pathlib import Path
import time
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
connecter_Class = connecter.aruba_os_telnet()

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            #  log the user in
            login(request, user)
            return redirect('/')
            # return render(request, 'appbase.html')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html',{'user_form': user_form})
     
    
def login_view(request):
    if request.method == "POST":
        user_form = AuthenticationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.get_user()
            #  log the user in
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
                # return render(request, 'appbase.html')
    else:
        user_form = AuthenticationForm()
    return render(request, 'login.html',{'user_form': user_form})

def logout_view(request):
    print("in logout")
    if request.method == "POST":
        logout(request)
        return redirect('/login')

@login_required(login_url="login")
def app_view(request):
    manual_data = list(Manual.objects.values())[0]
    # return HttpResponse(posts),'data')
    # print(manual_data)# = Manual.objects.all())
    try:
        current_user = request.user
        if request.method == 'POST':
            input_data = request.POST
            input_data = input_data.dict()
            print("input data",input_data)
            if input_data['odoo_id']:
                print("inside oddo function")
                odoo_data = connecter_Class.odoo_fetch_api(input_data)
                # print("@",odoo_data)
                # connecter_Class.data_store(input_data)
            else:
                print("inside other function")
                if(input_data['switch_type'] == "aruba"):
                    print("hello aruba")
                    output_1 = connecter_Class.add()
                    print("output1",output_1)
                    if output_1 == "success":
                        output_2 = connecter_Class.sub()
                        print("output2",output_2)
                        if output_2 ==  "success":
                            output_3 = connecter_Class.mul()
                            print("output3",output_3)
                            if output_3 ==  "success":
                                output_4 = connecter_Class.delete()
                                print("output4",output_4)
                                if output_4 ==  "success":
                                    print("all done successfully")
                                else:
                                    print("exception in output4", output_4)            
                            else: 
                                print("exception in output3", output_3)    
                        else:
                            print("exception in output2", output_2)    
                    else:
                        print("exception in output1", output_1)
                            
                    # connecter_Class.data_store(input_data)
                    # connecter_Class.connect_telnet()
                    # connecter_Class.configure_new_manager_password()
                    # connecter_Class.configure_ip()
                    # connecter_Class.configure_ssh()
                    # connecter_Class.get_ssh_data()
                    # connecter_Class.firmware_upgrade()
                    # connecter_Class.copy_primaryflash_secondaryflash()
                    # connecter_Class.reload()
                else: 
                    print("hello aruba cx")
                
        return render(request, 'appbase.html',{'current_user':current_user,"manual_data":manual_data})
    except Exception:
        return render(request, 'appbase.html',{'current_user':current_user,"manual_data":manual_data})

def edit_manual(request):
    return render(request, 'edit_manual.html')
         
def update_manual_data(request):
    print("update_data")
    if request.method == 'POST':
        input_data = request.POST
        input_data = input_data.dict()
        print("input data",input_data)

def home_view(request):
    return redirect('/login')