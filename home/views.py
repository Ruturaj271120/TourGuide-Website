from django.shortcuts import render
from home.models import Product
from math import ceil
from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import Contact,Orders,OrderUpdate,Blogpost
from django.contrib import messages
import json
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout


# Create your views here.
def index(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')

def guide(request):
    myposts= Blogpost.objects.all()
    print(myposts)
    return render(request,'guide.html',{'myposts': myposts})


def blockpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return render(request,'blockpost.html',{'post':post})

def contact(request):
    thank=False
    if request.method =="POST":
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        contact=Contact(name=name, email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        thank=True
    return render(request,'contact.html',{'thank':thank})
    

def napal(request):
    products= Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds } 
    return render(request,'napal.html',params)


def productView(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'productView.html', {'product':product[0]})




def checkout(request):
    if request.method =="POST":
        items_json=request.POST.get('itemsJson')
        amount=request.POST.get('amount')
        name=request.POST.get('name')
        email=request.POST.get('email')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')
        phone=request.POST.get('phone')
        date=request.POST.get('date')
        order=Orders(items_json=items_json,name=name, email=email,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update= OrderUpdate(order_id= order.order_id, update_desc="Your Guide will update the message")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id': id})
    return render(request, 'checkout.html')



def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'tracker.html')



def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query.lower(), item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)




def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email1']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            thank3=True
            return render(request,'index.html',{'thank3':thank3})
       

        if not username.isalnum():
            thank4=True
            return render(request,'index.html',{'thank4':thank4})
          
        if (pass1!= pass2):
            thank5=True
            return render(request,'index.html',{'thank5':thank5})
         
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        thank6=True
        return render(request,'index.html',{'thank6':thank6})

    else:
        return HttpResponse("page not found")




def handeLogin(request):
    if request.method=="POST":
      
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
           
            thank2=True
            return render(request,'index.html',{'thank2':thank2})
            
        else:
           
            thank1=True
            return render(request,'index.html',{'thank1':thank1})

    return HttpResponse("page not found")



def handelLogout(request):
    logout(request)
    thank7=True
    return render(request,'index.html',{'thank7':thank7})
    