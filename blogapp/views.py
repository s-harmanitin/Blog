from django.shortcuts import render,redirect
from .models import blog,userdetails
from .forms import blogform
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



# Create your views here.

# Create your views here.


@login_required(login_url='login')
def read(request):
    if request.user.is_authenticated:
        read_data = blog.objects.all()
        paginator = Paginator(read_data, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home.html',{'read_data':page_obj})
    else:
        return render(request,'home.html')




# def home(request):
#     if request.user.is_authenticated:
#         data = tut.objects.all()
#         paginator = Paginator(data, 6)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         return render(request, 'home.html', {'data': page_obj})
#     else:
#         return render(request, 'home.html',)


def create(request):
    if request.method == 'GET':
        form = blogform()
        return render(request,'create.html',{'form':form})
    else:
        form = blogform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')


def update(request,id):
    if request.method =='GET':
        data = blog.objects.get(id=id)
        form = blogform(instance=data)
        return render(request,'create.html',{'form':form})
    else:
        data = blog.objects.get(id=id)
        form = blogform(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('home')


def delete(request,id):
    del_data = blog.objects.get(id=id)
    del_data.delete()
    return redirect('home')

    
def readmore(request,id):
    readmore = blog.objects.get(id=id)
    return render(request,'readmore.html',{"readmore":readmore})



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if len(first_name)>10:
            messages.info(request,'first name cannot be more than 10letters')
            return redirect('register')
        
        if len(password)>5:
            special_characters = "!@#$%^&*()-+?_=,<>./"
            for i in special_characters:
                if i in password:
                    if password == password1:
                        if User.objects.filter(username=username).exists():
                            messages.info(request,'username already exites')
                            return redirect('register')
                        elif User.objects.filter(email=email).exists():
                            messages.info(request,'Email already exist')
                            return redirect('register')
                        else:
                            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
                            user.save()
                            return redirect('login')
                    else:
                        messages.info(request,'password not matching')
                        return redirect('register')
                else:
                    messages.info(request,'passwaord must contains any special charactor')
                    return redirect('register')
        else:
            messages.info(request,'password must be grater than 6 letters')
            return redirect('register')


    else:
        return render(request,'register.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')

        else:
            messages.info(request,'username/passsword not matching')
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

        
def changepassword(request):
    if request.method =='GET':
        cp = PasswordChangeForm(User=request.User)
        return render(request,'changepass.html',{'cp':cp})
    elif request.method == 'POST':
        aa = PasswordChangeForm(user=request.user,data=request.POST)
        if aa.is_valid():
            user = aa.save()
            update_session_auth_hash(request,user)
            return redirect('home')


def search(request):
    inp_search = request.POST['inp_search']
    read_data = blog.objects.filter(heading__contains = inp_search)
    return render(request,'home.html',{'read_data':read_data})


def first(request):
    return render(request,'first.html')



def profile(request):
    if request.user.is_authenticated:
        if userdetails.objects.filter(name__exact = request.user).exists():
            a = blog.objects.filter(upload_by = request.user)
            b = userdetails.objects.get(name__exact = request.user)
            return render(request,'profile.html',{'form_a':a,'b':b})
        else:
            return redirect('adduserdata')
    else:
        return redirect('login')
        

def adduserdata(request):
    if request.user.is_authenticated:
        if userdetails.objects.filter(name__exact = request.user).exists():
            return redirect('profile')
        else:
            if request.method == "POST":
                name = request.user
                profileimage = request.FILES['profileimage']
                phonenumber = request.POST['phonenumber']
                
                userdata = userdetails(name=name,profileimage=profileimage,phonenumber=phonenumber)
                if len(phonenumber)>10:
                    return redirect('profile')
                else :
                    userdata.save()
                return redirect('profile')
            return render(request,'adduserprofile.html')

def category(request):
    catdata = blog.objects.filter(tag__exact = 6)
    catdata1 = blog.objects.filter(tag__exact = 10)
    catdata2 = blog.objects.filter(tag__exact = 11)
    catdata3 = blog.objects.filter(tag__exact = 12)
    return render(request,'cat.html',{'catdata':catdata,'catdata1':catdata1,'catdata2':catdata2,'catdata3':catdata3})
    # return render(request,'cat.html',{'catdata':catdata},{'catdata1':catdata1},{'catdata2':catdata2},{'catdata3':catdata3})


def updateprofile(request,id):
    if request.user.is_authenticated:
        userdata = userdetails.objects.get(id=id)
        if request.method =='POST':
            profile = request.FILES['profileimage']
            a = userdetails(id=id,name=userdata.name,profileimage=profile ,phonenumber=userdata.phonenumber)
            a.save()
            return redirect('profile')
        return render(request,'adduserprofile.html',{'data':userdata})
    return redirect('login')