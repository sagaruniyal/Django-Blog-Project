from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout



# Create your views here.
#Html pages
def home(request):
    #fetch top 3 post based on the no. of views
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'home/home.html',context)
def about(request):
    return render(request,'home/about.html')
    #return HttpResponse('This is about')
def contact(request):
    #messages.error(request, 'Welcome to Contact')
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your message has been successfully sent")
    return render(request,'home/contact.html')
    #return HttpResponse('This is contact')
def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostContent=Post.objects.filter(content__icontains=query)
        allPosts=allPostsTitle.union(allPostContent)
    if allPosts.count() == 0:
        messages.warning(request,"No search results found . Please Refine your query")
    params={'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)
    #return HttpResponse('This is search')
#Authentication Apis
def handleSignup(request):
    if request.method == 'POST':
        #Get the POST Pasrameters
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check for errornous input
        #username should be under 10 characters
        if len(username)>10:
             messages.error(request,"Username must be under 10 characters")
             return redirect('home')


        #username should be alphanumeric
        if not username.isalnum():
             messages.error(request,"Username should only contain letters and number")
             return redirect('home')


        #password should match
        if pass1!=pass2:
            messages.error(request,"Password do not match")
            return redirect('home')

        #Create the User
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your iCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
    
def handleLogin(request):
    if request.method == 'POST':
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials,Please try again")
            return redirect('home')
    
    return HttpResponse('404 - Not Found')
            
        


def handleLogout(request):
    logout(request)
    messages.success(request,"successfully Logged out")
    return redirect('home')
    return HttpResponse("logedout")

