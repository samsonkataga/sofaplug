from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from app1.forms import *
from django.contrib.auth import authenticate,login,logout
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View
#from django.views import generic
#from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request,category_slug=None):
	category = None
	categories = Category.objects.all()
	item = Item.objects.all().order_by('-id')
	if category_slug:
		category = get_object_or_404(Category,slug=category_slug)
		item = item.filter(category=category)
	context = {
		'item':item,
		'categories':categories,
		'category':category
	}

	return render(request, 'app1/home.html',context)

def ourproduct(request,category_slug=None):
	category = None
	categories = Category.objects.all().order_by('-id')
	item = Item.objects.all().order_by('-id')
	if category_slug:
		category = get_object_or_404(Category,slug=category_slug)
		item = item.filter(category=category)
	context = {
		'item':item,
		'categories':categories,
		'category':category
	}

	return render(request, 'app1/ourproduct.html',context)

def base(request):
	return render(request, 'app1/base.html')

def contact(request):
	form = ContactForm()
	if request.method=='POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Message sent successfully,thanks for contacting to us')
			return redirect('home')
	context = {
		'form':form
	}
	return render(request, 'app1/contact.html',context)

def settlement(request):
	form = SettlementForm()
	if request.method=='POST':
		form = SettlementForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'your detail updated successfully, we will contact with you')
			return redirect('order_summary')
	context = {
		'form':form
	}
	return render(request,'app1/settlement.html',context)


def signup(request):
	if request.method == 'POST':
		username=request.POST['username']
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		email=request.POST['username']
		password1=request.POST['password1']
		password2=request.POST['password2']

		myuser=User.objects.create_user(username,email,password1)
		myuser.first_name=firstname
		myuser.last_name=lastname
		myuser.save()
		messages.success(request,'You registered successfully')
		return redirect('signin')

	return render(request,'app1/signup.html')

def signin(request):

	if request.method == 'POST':
		username = request.POST['username']
		password1 = request.POST['password1']
		user = authenticate(username=username,password=password1)

		if user is not None:
			login(request,user)
			
			return render(request,'app1/home.html')

		else:
			messages.error(request,'Bad authenticate')
			return redirect('signin')


	return render(request,'app1/signin.html')

def signout(request):
	logout(request)
	messages.success(request,"you logged out successfully")
	return redirect('home')
	return render(request,'app1/signout.html')

def about(request):
	x = Leaders.objects.all()
	context = {
		'x':x
	}
	return render(request, 'app1/about.html',context)

def detailed_product(request,id):
	detailed_product = Item.objects.get(id=id)
	context = {
		'detailed_product':detailed_product
	}
	return render(request, 'app1/detailed_product.html',context)

def receivedmessage(request):
	x = Contact.objects.all()
	context = {
		'x':x
	}
	return render(request,'app1/receivedmessage.html',context)





def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item} was added to your Order")
            return redirect('order_summary')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item} was added to your Order")
        return redirect('order_summary')

def remove_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.id).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item.title} was removed from your Order")
                
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active order!")
        return redirect('order_summary')

class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order':order
        }
        return render(self.request, 'app1/order_summary.html',context)
def remove_single_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__id=item.id).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item}'s quantity was updated")
            return redirect('order_summary')
        else:
            messages.info(request, f"{item.title} was not in your Order")
            return redirect('order_summary')
    else:
        messages.info(request, "You don't have an active Order!")
        return redirect('order_summary')
class ItemPost(CreateView):
	model=Item
	form_class=ItemForm
	template_name= 'app1/item_view.html'
	success_url=reverse_lazy('home')