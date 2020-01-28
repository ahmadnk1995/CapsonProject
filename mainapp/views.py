from django.shortcuts import render , redirect  ,HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView , ListView , DetailView ,CreateView
from mainapp.models import Category , Product , Order  , OldOrders , Comment
from mainapp import models
from django.contrib.auth.models import User,auth
import datetime
from django.urls import reverse_lazy
from django.conf import settings
print(settings.REC)
#models.ProductKNN.objects.all().delete()
#models.ProductKNN.fill()

class MainView(TemplateView):
    '''this view  to open the main page '''
    template_name="main.html"

class ContactView(TemplateView):
    '''this view  to open the contant page '''
    template_name="contact.html"
   
def CheckoutView(request):
    '''this view  to open the checkout page '''
    return render (request,"checkout.html")

def RegestrView(request):
    '''this view  to open the regstration  page '''
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        user_name=request.POST['user_name']
        password=request.POST['password']
        email=request.POST['email']
        print(user_name)
        if User.objects.filter(username=user_name).exists():
            messages.info(request,'User Name Taken')
            return redirect('reg')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email Taken')
            return redirect('reg')
        elif user_name=="":
            messages.info(request,'Enter User Name')
            return redirect('reg')
        elif password=="":
            messages.info(request,'Enter Password')
            return redirect('reg')
        else:
            user=User.objects.create_user(username=user_name,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            print('user created')
            return redirect('login')
        return redirect('/')
    return render(request,"register.html")

def LoginView(request):
    '''this view  to open the login  page '''
    if request.method=="POST":
        user_name=request.POST['user_name']
        password=request.POST['password']
        user=auth.authenticate(username=user_name,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('main')
        else:
            messages.info(request,'UserName or password are not correct')
            return redirect('login')
    else:
        return render(request,"login.html")

def LogoutView(request):
    '''this view  to logout the loged in user '''
    auth.logout(request)
    return redirect (reverse_lazy("main"))

class CategoriesView(ListView):
    '''this view  to open the Category page and show all Categories to  the user  '''
    template_name="category.html"
    model=Category
    fildes="__all__"

def ProductsListView(request,fk):
    context={}
    product = Product.objects.filter(category=fk)
    context['Products'] = product
    return render(request,"products.html",context=context)

class ProductDetailView(DetailView):
    '''this view show a product details '''
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Comment']=Comment.objects.filter(product=self.kwargs['pk'])
        return context

def chartView(request):
    '''this view  to open the cart page and show all products in it   '''
    if request.user.id == None:
            return redirect('login')
    else:
        context = {}
        orders = Order.objects.filter(user=request.user)
        orderssum=0
        for i in orders:
            orderssum+=i.product.price
        context['orders']=orders
        context['orderssum']=orderssum

        if request.method=="POST":
            for i in orders:
                new_order=OldOrders()
                new_order.user=i.user
                new_order.product=i.product
                new_order.date=datetime.datetime.now()
                new_order.save()
                i.delete()
        return render(request,"cart.html",context)

def AddToChartView(request,product_id):
    '''this view  used to att a product to the cart  '''
    getproduct=Product.objects.get(id=product_id)   
    if request.method=="POST":
        if request.user.id == None:
            return redirect('login')
        else:
            order = Order()
            order.product=getproduct
            order.user=request.user
            order.date=datetime.datetime.now()
            order.save()
            return redirect (reverse_lazy("cart"))
    return redirect (reverse_lazy("cart"))

def DeleteFromChartView(request,dproduct_id):
    '''this view  used to delete  a product to the cart  '''
    order=Order.objects.filter(user=request.user)
    if request.method=="POST":
        for i in order:
            if i.product.id==dproduct_id:
                i.delete()
                break
    return redirect (reverse_lazy("cart"))

def searchView(request):
    '''this view  used to search for a a product buy name  '''
    context={}
    if request.method=="POST":
        getproducts=Product.objects.filter(name__contains=request.POST['message'])
        context['objects']=getproducts

    return render(request,"search.html",context=context)

def Addcomment(request, pid):
    '''this view  used to add a comment to a product   '''
    if request.user.id == None:
            return redirect('login')
    else:
        if request.method=="POST":
            getproduct=Product.objects.get(id=pid)   
            comment=Comment()
            comment.user=request.user
            comment.date=datetime.datetime.now()
            comment.text= request.POST['message']
            comment.product=getproduct
            comment.save()
        return redirect (reverse_lazy("product", args=(str(pid))))