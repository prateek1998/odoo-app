from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
import sweetify
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from .models import Manual, Firmware_Records
from Switches_Connecter import connecter
from pathlib import Path
import json
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
    firmware_tableArray = list(Firmware_Records.objects.values())
    # print(firmware_tableArray)
    try:
        if request.method == 'POST':
            input_data = request.POST
            input_data = input_data.dict()
            # print("input data",input_data)
            if input_data['odoo_id']:
                print("inside oddo function")
                odoo_data = connecter_Class.odoo_fetch_api(input_data)
                # print("@",odoo_data)
                # connecter_Class.data_store(input_data)
            else:
                print("inside other function")
                if(input_data['switch_type'] == "aruba"):
                    print("hello aruba")
                    # output_1 = connecter_Class.add()
                    # print("output1",output_1)
                    # if output_1 == "success":
                    #     output_2 = connecter_Class.sub()
                    #     print("output2",output_2)
                    #     if output_2 ==  "success":
                    #         output_3 = connecter_Class.mul()
                    #         print("output3",output_3)
                    #         if output_3 ==  "success":
                    #             output_4 = connecter_Class.delete()
                    #             print("output4",output_4)
                    #             if output_4 ==  "success":
                    #                 print("all done successfully")
                    #             else:
                    #                 print("exception in output4", output_4)            
                    #         else: 
                    #             print("exception in output3", output_3)    
                    #     else:
                    #         print("exception in output2", output_2)    
                    # else:
                    #     print("exception in output1", output_1)
                    # print("ASDAsdad")
                            
                    connecter_Class.data_store(input_data)
                    connecter_Class.connect_telnet()
                    connecter_Class.configure_new_manager_password()
                    connecter_Class.configure_ip()
                    connecter_Class.configure_ssh()
                    connecter_Class.get_ssh_data()
                    connecter_Class.firmware_upgrade()
                    connecter_Class.copy_primaryflash_secondaryflash()
                    connecter_Class.reload()
                    sweetify.error(request, 'Firmware Updated Successfully', text='Good job! You successfully updated the Firmware',icon='success', persistent="Ok")
                    
                    # <!-- {% for firmware_entry in firmware_tableArray %} -->
                                                
                else: 
                    print("hello aruba cx")
                
        return render(request, 'appbase.html',{"manual_data":manual_data,"firmware_tableArray":firmware_tableArray})
    except Exception:
        return render(request, 'appbase.html',{"manual_data":manual_data,"firmware_tableArray":firmware_tableArray})

def edit_manual(request):
    manual_data = list(Manual.objects.values())[0]
    if request.method == 'POST':
        try:
            input_data = request.POST
            input_data = input_data.dict()
            manual_data = Manual.objects.get(id=manual_data['id'])
            # print(manual_data.proxy_ip)
            manual_data.proxy_ip = input_data['proxy_ip']
            manual_data.tftp_server = input_data['tftp_server']
            manual_data.save()
            sweetify.success(request, 'Updated Successfully', text='Good job! You successfully updated the manual data',icon='success',persistent="Ok")
            return home_view(request)
        except Exception as e:
            error_msg = 'Check error: '+ str(e)
            sweetify.error(request, 'Something went wrong!', text=error_msg,icon='error', persistent="Ok")
            return home_view(request)
        return render(request, 'appbase.html',{"manual_data":manual_data})

def home_view(request):
    return redirect('/')