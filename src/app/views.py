from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from Switches_Connecter import connecter
from pathlib import Path

# Create your views here.

BASE_DIR = Path(__file__).resolve().parent.parent
connecter_Class = connecter.aruba_os_telnet();

def Login_Page(request):
    return render(request, 'login.html')

def Register_Page(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'appbase.html')
    else: 
        user_form = UserCreationForm()
    return render(request, 'register.html',{'user_form': user_form})

def App_Page(request):
    try:
        # if request.method == 'POST':
        #     if request.POST['odoo_id']   == '':
        #         return render(request, 'appbase.html', {'error': 'Please fill all the fields '})
        odoo_id = request.POST['odoo_id']
        print("getting odoo id",odoo_id);
        connecter_Class.odoo_fetch_api(odoo_id);
        return render(request, 'appbase.html')
    except Exception:
        return render(request, 'appbase.html')
    

def Home_Page(request):
    return redirect('/login')