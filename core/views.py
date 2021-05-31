from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import *
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group
from .decorators import allowed_users, admin_only
from django.contrib.auth.decorators import user_passes_test
from django import template
import datetime
import random
import string
from django.http import JsonResponse
from .sms import *
from django.views.decorators.csrf import csrf_exempt


#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "STATIC START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class CheckoutView(View):
    def get(self, *args, **kwargs):
        customer = self.request.user.customer
        cat = Category.objects.filter(is_active=True)
        res = PartnerStore.objects.filter(is_active=True)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False) 
            form_choice = ChoiceForm()
            rate = Rate.objects.filter(is_active=True)
            item_cat = ItemCategory.objects.filter(is_active=True)
            context = {
                'order': order,
                'customer': customer,
                'form_choice': form_choice,
                'rate': rate,
                'cat':cat,
                'res':res,
                'item_cat':item_cat
            }
            return render(self.request, "checkout.html", context)
            return render(self.request, "cart.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")
            
    def post(self, *args, **kwargs):
        if self.request.method == 'POST' and 'btnAddress' in self.request.POST:
            form_choice = ChoiceForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                print(self.request.POST)
                if form_choice.is_valid():
                    
                    latitude = self.request.POST['lat2']
                    longitude = self.request.POST['lon2']
                    default_complete_address = self.request.POST['default_complete_address']
                    default_address_line_2 = self.request.POST['default_address_line_2']

                    billingaddress = BillingAddress(
                    user = self.request.user,
                    latitude=latitude,
                    longitude=longitude,
                    complete_address=default_complete_address,
                    address_line_2=default_address_line_2
                    )
                    billingaddress.save()
                    order.shipping_address = billingaddress

                    payment_option = form_choice.cleaned_data.get('payment_option')
                    payment = Payment()
                    payment.user = self.request.user
                    payment.amount = order.get_total()
                    payment.payment_choice = payment_option
                    payment.save()
                    order.ordered = True
                    order.status = 'Pending'
                    
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()
                    messages.success(self.request, "Order was successful")
                    return redirect("core:customer_order_history")       
                else:
                    messages.warning(self.request, "Invalid payment option select")
                    return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order")
                return redirect("core:order-summary")
        if self.request.method == 'POST' and 'btnNewAddress' in self.request.POST:
            form_choice = ChoiceForm(self.request.POST or None)
            try:
                order = Order.objects.get(user=self.request.user, ordered=False)
                print(self.request.POST)
                if form_choice.is_valid():
                    
                    latitude = self.request.POST['new_lat']
                    longitude = self.request.POST['new_lon']
                    complete_address = self.request.POST['complete_address']
                    address_line_2 = self.request.POST['address_line_2']

                    billingaddress = BillingAddress(
                    user = self.request.user,
                    latitude=latitude,
                    longitude=longitude,
                    complete_address=complete_address,
                    address_line_2=address_line_2
                    )
                    billingaddress.save()
                    order.shipping_address = billingaddress

                    payment_option = form_choice.cleaned_data.get('payment_option')
                    payment = Payment()
                    payment.user = self.request.user
                    payment.amount = order.get_total()
                    payment.payment_choice = payment_option
                    payment.save()
                    order.ordered = True
                    order.status = 'Pending'
                    
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()
                    messages.success(self.request, "Order was successful")
                    return redirect("core:customer_order_history")       
                else:
                    messages.warning(self.request, "Invalid payment option select")
                    return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.error(self.request, "You do not have an active order")
                return redirect("core:order-summary")

class HomeView(ListView):
    def get(self, *args, **kwargs):
        items = Item.objects.filter(is_active=True)
        partnerstore = PartnerStore.objects.filter(is_active=True)
        slide = Slide.objects.filter(is_active=True)

        context = {     
            'items':items,
            'partnerstore':partnerstore,
            'slide':slide,
        }
        
        #return render(self.request, "index.html", context)
        return render(self.request, "index1.html", context)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            cat = Category.objects.filter(is_active=True)
            res = PartnerStore.objects.filter(is_active=True)
            item_cat = ItemCategory.objects.filter(is_active=True)
            context = {
                'object': order,
                'cat': cat,
                'res': res,
                'item_cat': item_cat
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(user=self.request.user, ordered=False)
            attr = self.request.POST['attr']
            order_item.selected_attr = attr
            order_item.save()
            return redirect("core:order-summary")
        except ObjectDoesNotExist:
            messages.error(self.request, "Please choose an attribute")
            return redirect("core:order-summary")

def AllCategoryView(request):
    cat = Category.objects.filter(is_active=True)
    res = PartnerStore.objects.filter(is_active=True)
    item_cat = ItemCategory.objects.filter(is_active=True)
    item = Item.objects.filter(is_active=True)
    form = OthersForm()
    if request.method == 'POST':
        form = OthersForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data.get('note')
            payment_option = form.cleaned_data.get('payment_option')  
            other = Other(
                user=request.user,
                note=note,
                payment_option=payment_option
            )

            order = Order(
                user=request.user,
                ordered = True,
                date_ordered = timezone.now(),
                status = 'Pending'
            )
            payment = Payment(
                user = request.user,
                amount = '0',
                payment_choice = payment_option
            )
            payment.save()

            other.save()
            order.other = other
            order.payment = payment
            order.save()  
            messages.success(request, 'Sugo successfully added!')
            return redirect('core:customer_dashboard')
    item = Item.objects.all()
    store = PartnerStore.objects.all()
    context = {
        'object_list': item,
        'store': store,
        'form': form,
        'cat':cat,
        'res':res,
        'item_cat':item_cat,
        'item':item
    }
    return render(request, "allcategories.html", context)

def OtherView(request):
    cat = Category.objects.filter(is_active=True)
    res = PartnerStore.objects.filter(is_active=True)
    item_cat = ItemCategory.objects.filter(is_active=True)

    form = OthersForm()
    if request.method == 'POST':
        form = OthersForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data.get('note')
            payment_option = form.cleaned_data.get('payment_option')  
            other = Other(
                user=request.user,
                note=note,
                payment_option=payment_option
            )

            order = Order(
                user=request.user,
                ordered = True,
                date_ordered = timezone.now(),
                status = 'Pending'
            )
            payment = Payment(
                user = request.user,
                amount = '0',
                payment_choice = payment_option
            )
            payment.save()

            other.save()
            order.other = other
            order.payment = payment
            order.save()  
            messages.success(request, 'Sugo successfully added!')
            return redirect('core:customer_dashboard')
    item = Item.objects.all()
    store = PartnerStore.objects.all()
    context = {
        'object_list': item,
        'store': store,
        'form': form,
        'cat':cat,
        'res':res,
        'item_cat':item_cat
    }
    return render(request, "others.html", context)

 
class ItemDetailView(DetailView):
    model = Item
    template_name = "product-detail.html"

class PartnerDetailView(View):
    def get(self, *args, **kwargs):
        store = PartnerStore.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(store=store, is_active=True)
        cat = Category.objects.filter(is_active=True)
        res = PartnerStore.objects.filter(is_active=True)
        item_cat = ItemCategory.objects.filter(is_active=True)
        context = {
            'object_list': item,
            'store': store,
            'store_title': store,
            'store_description_short': store.description_short,
            'store_profile_pic': store.profile_pic,
            'cat':cat,
            'res':res,
            'item_cat':item_cat
        }
        return render(self.request, "partner_detail.html", context)

class CategoryView(View):
    def get(self, *args, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(is_active=True)
        store = PartnerStore.objects.filter(is_active=True)
        partnerstore = PartnerStore.objects.filter(is_active=True)

        form = OthersForm()
        if self.request.method == 'POST':
            form = OthersForm(self.request.POST)
            if form.is_valid():
                note = form.cleaned_data.get('note')
                payment_option = form.cleaned_data.get('payment_option')  
                other = Other(
                    user=self.request.user,
                    note=note,
                    payment_option=payment_option
                )

                order = Order(
                    user=self.request.user,
                    ordered = True,
                    date_ordered = timezone.now(),
                    status = 'Pending'
                )
                payment = Payment(
                    user = self.request.user,
                    amount = '0',
                    payment_choice = payment_option
                )
                payment.save()

                other.save()
                order.other = other
                order.payment = payment
                order.save()  
                messages.success(self.request, 'Sugo successfully added!')
                return redirect('core:customer_dashboard')
        
        context = {
            'form':form,
            'object_list': item,
            'store': store,
            'category_title': category.title,
            'partnerstore':partnerstore
        }
        return render(self.request, "category.html", context)

def adminsearch(request):
    if 'term' in request.GET:
        qs = Order.objects.filter(user__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request, "admin_dashboard.html")

def Contact_Us(request):
    
    return render(request, "contact.html")
#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "STATIC END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "CART START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        partnerstore=item.user.partnerstore
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item qty was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item was added to your cart.")
            return redirect("core:order-summary")
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(
            user=request.user, date_ordered=date_ordered)
        order.items.add(order_item)
        order.partnerstore = order_item.partnerstore
        order.save()
        messages.info(request, "Item was added to your cart.")
    return redirect("core:order-summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                partnerstore=item.user.partnerstore
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "Item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "u don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                partnerstore=item.user.partnerstore
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user dosent have an order
            messages.info(request, "You don't have an active order.")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user dosent have an order
        messages.info(request, "You don't have an active order.")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)
#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "CART END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "ADMIN START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
@login_required
@allowed_users(allowed_roles=['admin'])    
def AdminDashBoard(request):
    orders = Order.objects.all().order_by('-date_ordered')
    riders = Rider.objects.all()      
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total = 0

    for gross in orders.filter(status='Delivered'):
        total = gross.service_charge + gross.surcharge
        print(total)

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    mydate = datetime.datetime.now()

    context = {       
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'total':total,
        'riders':riders,
        'myFilter':myFilter,
        'ongoing':ongoing,
        'mydate':mydate
    }
    #return render(request, "admin/admin_dashboard.html", context)
    return render(request, "admin/dashboard_admin.html", context)

def AllAdmins(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    admins = Admin.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')
            user = form.save()
            group = Group.objects.get(name='admin')
            user.groups.add(group)

            admin = Admin(
                user=user,
                is_active=True,
                email=user.email,
                contact=contact
            )
            user = admin.save()

    context = {
        'admins':admins,
        'form':form,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_admins.html", context)

def AllStores(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partners = PartnerStore.objects.all()
    partnercnt = partners.count()

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')
            user = form.save()
            group = Group.objects.get(name='partner')
            user.groups.add(group)

            partner = PartnerStore(
                user=user,
                is_active=True,
                email=user.email,
                contact=contact
            )
            user = partner.save()

    context = {
        'form':form,
        'partners':partners,
        'partnercnt':partnercnt,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_stores.html", context)

def AllRiders(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    rider = Rider.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            contact = form.cleaned_data.get('contact')
            user = form.save()
            group = Group.objects.get(name='rider')
            user.groups.add(group)

            riders = Rider(
                user=user,
                is_active=True,
                email=user.email,
                contact=contact
            )
            user = riders.save()

    context = {
        'rider':rider,
        'form':form,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_riders.html", context)

def AllCustomers(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    customer = Customer.objects.all()

    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_customers.html", context)

def AllCategory(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    cat = Category.objects.all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:all_categories")

    context = {
        'cat':cat,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'form':form
    }
    return render(request, "admin/all_category.html", context)

def AllItems(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    itms = Item.objects.all()

    form = ItemForm()
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("core:all_items")

    context = {
        'itms':itms,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'form':form
    }
    return render(request, "admin/all_items.html", context)

def AllDispatchers(request):
    orders = Order.objects.all().order_by('-date_ordered')   
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()

    dispatchers = Dispatcher.objects.all()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact = form.cleaned_data.get('contact')
            group = Group.objects.get(name='dispatcher')
            user.groups.add(group)

            dispatcher = Dispatcher(
                user=user,
                is_active=True,
                email=user.email,
                contact=contact
            )
            user = dispatcher.save()
            return redirect("core:all_dispatchers")

    context = {
        'dispatchers':dispatchers,
        'form':form,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_dispatchers.html", context)

def PendingOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    pend = orders.filter(status="Pending")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    admin = Admin.objects.filter(user=request.user)

    context = {
        'pend':pend,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt,
        'admin':admin
    }
    return render(request, "admin/pending_order.html", context)

def OnGoingOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    ong = orders.filter(status="On Going")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'ong':ong,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "admin/ongoing_order.html", context)

def DeliveredOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    dlv = orders.filter(status="Delivered")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'dlv':dlv,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "admin/delivered_order.html", context)

def AllOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "admin/all_order.html", context)

def AllOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "admin/all_order.html", context)
    

@login_required
@allowed_users(allowed_roles=['admin', 'dispatcher']) 
def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    mydate = datetime.datetime.now()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.total = order.get_total_payment()
            order.save()
            if order.status == "On Going":
                order.rider.status = "Unavailable"
                order.rider.save()
                order.save()
            else:
                order.rider.status = "Available"
                order.rider.save()
                order.save()
            messages.info(request, "Order was successfully updated.")
            return redirect("core:pending_order")
    context = {
        'form':form,
        'mydate':mydate
    }
    return render(request, "admin/update_order.html", context)

def UserAdminProfile(request):
    ads = Admin.objects.get(user=request.user, is_active=True)
    form1 = AdminForm(instance=ads)

    orders = Order.objects.all().order_by('-date_ordered')
    dlv = orders.filter(status="Delivered")
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    
    if request.method == 'POST' and 'btnSetting' in request.POST:
        form1 = AdminForm(request.POST, request.FILES, instance=ads)
        if form1.is_valid():
            form1.save()

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        ads.complete_address = complete_address
        ads.address_line_2 = address_line_2
        ads.latitude = latitude
        ads.longitude = longitude
        ads.save()

    context = {
        'form1':form1,
        'dlv':dlv,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'orders':orders,
        'ads':ads
    }
    return render(request, "admin/user-profile.html", context)

class PartnerView(View):
    def get(self, *args, **kwargs):
        store = PartnerStore.objects.get(slug=self.kwargs['slug'])
        item = Item.objects.filter(store=store, is_active=True)
        partner = PartnerStore.objects.all()
        partnercnt = partner.count()
        context = {
            'object_list': item,
            'store': store,
            'store_title': store,
            'store_description_short': store.description_short,
            'store_profile_pic': store.profile_pic,
            'partner':partner,
            'partnercnt':partnercnt
        }
        return render(self.request, "admin/partner.html", context)

@login_required
@allowed_users(allowed_roles=['admin']) 
def EditAdmin(request, pk):
    adm = Admin.objects.get(id=pk)
    form = AdminForm1(instance=adm)
    if request.method == 'POST':
        form = AdminForm1(request.POST, instance=adm)
        if form.is_valid():
            form.save()
            return redirect("core:all_admins")
        else:
            return redirect("/")
    context = {
        'form':form
    }
    return render(request, "admin/edit_admins.html", context)

@login_required
@allowed_users(allowed_roles=['admin']) 
def EditDispatcher(request, pk):
    dis = Dispatcher.objects.get(id=pk)
    form = EditDisForm(instance=dis)
    if request.method == 'POST':
        form = EditDisForm(request.POST, instance=dis)
        if form.is_valid():
            form.save()
            return redirect("core:all_dispatchers")
    context = {
        'form':form
    }
    return render(request, "admin/edit_dispatchers.html", context)

@login_required
@allowed_users(allowed_roles=['admin']) 
def EditRider(request, pk):
    rdr = Rider.objects.get(id=pk)
    form = EditRiderForm(instance=rdr)
    if request.method == 'POST':
        form = EditRiderForm(request.POST, instance=rdr)
        if form.is_valid():
            form.save()
            return redirect("core:all_Riders")
    context = {
        'form':form
    }
    return render(request, "admin/edit_dispatchers.html", context)

@login_required
@allowed_users(allowed_roles=['admin']) 
def EditPartner(request, pk):
    ptr = PartnerStore.objects.get(id=pk)
    form = EditPartnerForm(instance=ptr)
    if request.method == 'POST':
        form = EditPartnerForm(request.POST, instance=ptr)
        if form.is_valid():
            form.save()
            return redirect("core:all_stores")
    context = {
        'form':form
    }
    return render(request, "admin/edit_stores.html", context)

@login_required
@allowed_users(allowed_roles=['admin']) 
def EditCustomer(request, pk):
    cstmr = Customer.objects.get(id=pk)
    form = EditPartnerForm(instance=cstmr)
    if request.method == 'POST':
        form = EditPartnerForm(request.POST, instance=cstmr)
        if form.is_valid():
            form.save()
            return redirect("core:all_customers")
    context = {
        'form':form
    }
    return render(request, "admin/edit_customers.html", context)

    
@login_required
@allowed_users(allowed_roles=['admin']) 
def ShippingRate(request):
    rate = Rate.objects.get(is_active=True)
    form = ShippingRateForm(instance=rate)
    if request.method == 'POST':
        form = ShippingRateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            messages.info(request, "Shipping rate was successfully updated.")
            return redirect("core:shipping_rate")

    context = {
        'form':form
    }
    return render(request, "admin/shipping_rate.html", context)
#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "ADMIN END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                ###>>>>>>>>>>>>>>>>>>>>>>> "DISPATCHER START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
#@login_required
#@allowed_users(allowed_roles=['dispatcher'])    
def DispatchDashBoard(request):
    form = dis()
    orderItem = OrderItem.objects.all()
    billingAddress = BillingAddress.objects.all()   
    orders = Order.objects.all().order_by('-date_ordered')
    riders = Rider.objects.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total = 0
    for gross in orders:
        total += gross.service_charge
        print(total)
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    mydate = datetime.datetime.now()
    context = {   
        'riders':riders,    
        'orders':orders,
        'orderItem':orderItem,
        'billingAddress':billingAddress,
        'total':total,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'myFilter':myFilter,
        'mydate':mydate,
        'form':form
    }
    return render(request, "dispatcher/dispatcher_dashboard.html", context)

def DisPendingOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    pend = orders.filter(status="Pending")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    admin = Admin.objects.filter(user=request.user)

    context = {
        'pend':pend,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt,
        'admin':admin
    }
    return render(request, "dispatcher/pending_order.html", context)

def DisOnGoingOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    ong = orders.filter(status="On Going")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'ong':ong,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "dispatcher/ongoing_order.html", context)

def DisDeliveredOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    dlv = orders.filter(status="Delivered")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'dlv':dlv,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "dispatcher/delivered_order.html", context)

def DisAllOrder(request):
    orders = Order.objects.all().order_by('-date_ordered')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    
    context = {
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt
    }
    return render(request, "dispatcher/all_order.html", context)

#@login_required
#@allowed_users(allowed_roles=['dispatcher']) 
def Dispatch(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    mydate = datetime.datetime.now()
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.total = order.get_total_payment()
            order.save()
            if order.status == "On Going":
                order.rider.status = "Unavailable"
                order.rider.save()
                order.save()
            else:
                order.rider.status = "Available"
                order.rider.save()
                order.save()
            messages.info(request, "Order was successfully updated.")
            return redirect("core:dispatch_dashboard")
    context = {
        'form':form,
        'mydate':mydate
    }
    return render(request, "dispatcher/dispatch.html", context)

def DispatcherAccountSettings(request):
    dispatcher = Dispatcher.objects.get(user=request.user, is_active=True)
    form = DispatcherForm(instance=dispatcher)
  
    if request.method == 'POST' and 'btnSetting' in request.POST:
        form = DispatcherForm(request.POST, request.FILES, instance=dispatcher)
        if form.is_valid():
            form.save()

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        dispatcher.complete_address = complete_address
        dispatcher.address_line_2 = address_line_2
        dispatcher.latitude = latitude
        dispatcher.longitude = longitude
        dispatcher.save()

    context = {
        'form':form,
        'dispatcher':dispatcher
    }
    return render(request, "dispatcher/dispatcher_account_settings.html", context)
    
def DistanceCalculator(request):
    rate = Rate.objects.filter(is_active=True)
    partnerstore = PartnerStore.objects.all()
    
    context = {
        'rate':rate,
        'partnerstore':partnerstore
    }
    return render(request, "dispatcher/distance_calculator.html", context)
#-----------------------------------------------------------------------------------------------------------#
                ###>>>>>>>>>>>>>>>>>>>>>>> "DISPATCHER END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "RIDER START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
def RiderDashBoard(request):
    rider = request.user.rider
    orders = Order.objects.filter(rider=request.user.rider).order_by('-date_ordered')
    status = Rider.objects.filter(user=request.user)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    pend = orders.filter(status='Pending')
    ong = orders.filter(status='On Going')
    dlv = orders.filter(status='Delivered')
    total = 0
    for gross in orders:
        total += gross.service_charge
        print(total)
    context = {     
        'status':status,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'total':total,
        'pend':pend,
        'ong':ong,
        'dlv':dlv,
        'ongoing':ongoing,
    }
    #return render(request, "rider/rider_dashboard.html", context)
    return render(request, "rider/dashboard_rider.html", context)

@login_required
@allowed_users(allowed_roles=['rider']) 
def RidePendingOrder(request):
    rider = request.user.rider
    orders = Order.objects.filter(rider=request.user.rider).order_by('-date_ordered')
    status = Rider.objects.filter(user=request.user)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    pend = orders.filter(status='Pending')
    ong = orders.filter(status='On Going')
    dlv = orders.filter(status='Delivered')
    total = 0
    for gross in orders:
        total += gross.service_charge
        print(total)
    context = {     
        'status':status,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'total':total,
        'pend':pend,
        'ong':ong,
        'dlv':dlv,
        'ongoing':ongoing,
    }
    return render(request, "rider/pending_order.html", context)

@login_required
@allowed_users(allowed_roles=['rider']) 
def RideOngoingOrder(request):
    rider = request.user.rider
    orders = Order.objects.filter(rider=request.user.rider).order_by('-date_ordered')
    status = Rider.objects.filter(user=request.user)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    pend = orders.filter(status='Pending')
    ong = orders.filter(status='On Going')
    dlv = orders.filter(status='Delivered')
    total = 0
    for gross in orders:
        total += gross.service_charge
        print(total)
    context = {     
        'status':status,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'total':total,
        'pend':pend,
        'ong':ong,
        'dlv':dlv,
        'ongoing':ongoing,
    }
    return render(request, "rider/ongoing_order.html", context)

@login_required
@allowed_users(allowed_roles=['rider']) 
def RideDeliveredOrder(request):
    rider = request.user.rider
    orders = Order.objects.filter(rider=request.user.rider).order_by('-date_ordered')
    status = Rider.objects.filter(user=request.user)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    pend = orders.filter(status='Pending')
    ong = orders.filter(status='On Going')
    dlv = orders.filter(status='Delivered')
    total = 0
    for gross in orders:
        total += gross.service_charge
        print(total)
    context = {     
        'status':status,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'total':total,
        'pend':pend,
        'ong':ong,
        'dlv':dlv,
        'ongoing':ongoing,
    }
    return render(request, "rider/delivered_order.html", context)

@login_required
@allowed_users(allowed_roles=['rider']) 
def RiderOrderStatus(request, pk):
    order = Order.objects.get(id=pk)
    form = RiderOrderStatusForm(instance=order)
    rider = Rider.objects.get(user=request.user)
    if request.method == 'POST':
        form = RiderOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if order.status == 'On Going':
                rider.status = 'Unavailable'
                rider.save()
            else:
                rider.status = 'Available'
                rider.save()
            messages.info(request, "Order status was successfully updated.")
            return redirect("core:rider_dashboard")
    context = {
        'form':form
    }
    return render(request, "rider/rider_order_status.html", context)

@login_required
@allowed_users(allowed_roles=['rider']) 
def RiderStatus(request):
    rider = Rider.objects.get(user=request.user)
    form = RiderStatusForm(instance=rider)
    if request.method == 'POST':
        form = RiderStatusForm(request.POST, instance=rider)
        if form.is_valid():
            form.save()
            messages.info(request, "Status was successfully updated.")
            return redirect("core:rider_dashboard")
    context = {
        'form':form
    }
    return render(request, "rider/rider_order_status.html", context) 

def RiderAccountSettings(request):
    orders = Order.objects.filter(rider=request.user.rider).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()

    rider = Rider.objects.get(user=request.user, is_active=True)
    form1 = RiderForm(instance=rider)

    if request.method == 'POST' and 'btnProfile' in request.POST:
        form1 = RiderForm(request.POST, request.FILES, instance=rider)
        if form1.is_valid():
            form1.save()
    
    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        rider.complete_address = complete_address
        rider.address_line_2 = address_line_2
        rider.latitude = latitude
        rider.longitude = longitude
        rider.save()

    context = {
        'form1':form1,
        'rider':rider,
        'orders':orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'total_orders':total_orders,
    }

    return render(request, "rider/rider_account_settings.html", context)
#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "RIDER END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                ###>>>>>>>>>>>>>>>>>>>>>>> "PARTNER START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
@login_required
@allowed_users(allowed_roles=['partner'])     
def PartnerDashBoard(request): 
    order = request.user.partnerstore.order_set.all()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    ongoing = order.filter(status='On Going').count()
    total_orders = order.count()

    item = OrderItem.objects.all()
    total = 0;
    item_price = 0;
    orders = order.count()

    for item in item:
        if item.partnerstore == request.user.partnerstore:
            total += (item.item.price * item.quantity)
            print(total)

    
    context = {
        'item_price':item_price,
        'total':total,
        'item': item,
        'order': order,
        'orders':orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing': ongoing,
        'total_orders': total_orders,
    } 
    return render(request, "partner/partner_dashboard.html", context)

@login_required
@allowed_users(allowed_roles=['partner'])     
def PartnerItems(request):
    item = Item.objects.filter(user=request.user, is_active=True)
    order = Order.objects.filter(partnerstore=request.user.partnerstore)

    orders = request.user.partnerstore.order_set.all()
    delivered = order.filter(status='Delivered').count()
    pending = order.filter(status='Pending').count()
    ongoing = order.filter(status='On Going').count()
    total_orders = order.count()
    
    items = request.user
    form = PostForm(instance=items)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=items)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            name = form.cleaned_data.get('name')
            price = form.cleaned_data.get('price')
            stock_no = form.cleaned_data.get('stock_no')
            description_short = form.cleaned_data.get('description_short')
            description_long = form.cleaned_data.get('description_long')
            image = form.cleaned_data.get('image')
            is_active = form.cleaned_data.get('is_active')
            itemss = Item(
                user=request.user,
                store=request.user.partnerstore,
                category=category,
                name=name,
                price=price,
                stock_no=stock_no,
                description_short=description_short,
                description_long=description_long,
                image=image,
                is_active=is_active
            )
            itemss.save()
            messages.success(request, 'Item successfully posted!')
            return redirect('core:partner_items')
        
    context = {
        'item': item,
        'order': order,
        'form':form,
        'orders': orders,
        'delivered': delivered,
        'pending':pending,
        'ongoing': ongoing,
        'total_orders': total_orders
    } 
    return render(request, "partner/partner_items.html", context)

def UserPartnerProfile(request):
    partner1 = PartnerStore.objects.get(user=request.user, is_active=True)
    form1 = PartnerForm(instance=partner1)

    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    orders = Order.objects.all().order_by('-date_ordered')
    dlv = orders.filter(status="Delivered")
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()

    if request.method == 'POST' and 'btnSetting' in request.POST:
        form1 = PartnerForm(request.POST, request.FILES, instance=partner1)
        if form1.is_valid():
            form1.save()

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        partner1.complete_address = complete_address
        partner1.address_line_2 = address_line_2
        partner1.latitude = latitude
        partner1.longitude = longitude
        partner1.save()
        
    context = {
        'form1':form1,
        'partner':partner,
        'partner1':partner1,
        'partnercnt':partnercnt,
        'dlv':dlv,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'orders':orders,
        'total_orders':total_orders
    }
    return render(request, "partner/user-profile.html", context)


@login_required
@allowed_users(allowed_roles=['partner']) 
def UpdateItem(request, pk):
    item = Item.objects.get(id=pk)
    form = PostForm(instance=item)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item was successfully updated.")
            return redirect("core:partner_items")
    context = {
        'form':form
    }
    return render(request, "partner/update_item.html", context)

def PartnerPendingOrder(request):
    partners = request.user.partnerstore
    orders = Order.objects.filter(partnerstore=partners).order_by('-date_ordered')
    pend = orders.filter(status="Pending")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    partner = PartnerStore.objects.all()
    partnercnt = partner.count()
    admin = Admin.objects.filter(user=request.user)

    context = {
        'pend':pend,
        'orders':orders,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'partner':partner,
        'partnercnt':partnercnt,
        'admin':admin
    }
    return render(request, "partner/pending_order.html", context)

def PartnerOnGoingOrder(request):
    partners = request.user.partnerstore
    orders = Order.objects.filter(partnerstore=partners).order_by('-date_ordered')
    ong = orders.filter(status="On Going")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    
    context = {
        'ong':ong,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "partner/ongoing_order.html", context)

def PartnerDeliveredOrder(request):
    partners = request.user.partnerstore
    orders = Order.objects.filter(partnerstore=partners).order_by('-date_ordered')
    dlv = orders.filter(status="Delivered")
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    
    context = {
        'dlv':dlv,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "partner/delivered_order.html", context)


def PartnerAllOrder(request):
    partners = request.user.partnerstore
    orders = Order.objects.filter(partnerstore=partners).order_by('-date_ordered')
    all = orders.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    
    context = {
        'all':all,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing
    }
    return render(request, "partner/all_order.html", context)
#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "PARTNER END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#





#-----------------------------------------------------------------------------------------------------------#
                 ###>>>>>>>>>>>>>>>>>>>>>>> "CUSTOMER START" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#
@login_required
@allowed_users(allowed_roles=['customer']) 
def CustomerDashBoard(request):
    customer = request.user.customer
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()
    cust = Customer.objects.filter(user=request.user)
    pend = orders.filter(user=request.user, status='Pending')
    ong = orders.filter(user=request.user, status='On Going')
    dlv = orders.filter(user=request.user, status='Delivered')

    context = {
        'customer':customer,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'orders':orders,
        'cust':cust,
        'ongoing':ongoing,
        'pend':pend,
        'ong':ong,
        'dlv':dlv
    }
    #return render(request, "customer/customer_dashboard.html", context)
    return render(request, "customer/dashboard_customer.html", context)

@login_required
@allowed_users(allowed_roles=['customer']) 
def CustPendingOrder(request):
    customer = request.user.customer
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()
    cust = Customer.objects.filter(user=request.user)
    pend = orders.filter(user=request.user, status='Pending')
    ong = orders.filter(user=request.user, status='On Going')
    dlv = orders.filter(user=request.user, status='Delivered')

    context = {
        'customer':customer,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'orders':orders,
        'cust':cust,
        'ongoing':ongoing,
        'pend':pend,
        'ong':ong,
        'dlv':dlv
    }
    return render(request, "customer/pending_order.html", context)

@login_required
@allowed_users(allowed_roles=['customer']) 
def CustOngoingOrder(request):
    customer = request.user.customer
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()
    cust = Customer.objects.filter(user=request.user)
    pend = orders.filter(user=request.user, status='Pending')
    ong = orders.filter(user=request.user, status='On Going')
    dlv = orders.filter(user=request.user, status='Delivered')

    context = {
        'customer':customer,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'orders':orders,
        'cust':cust,
        'ongoing':ongoing,
        'pend':pend,
        'ong':ong,
        'dlv':dlv
    }
    return render(request, "customer/ongoing_order.html", context)

@login_required
@allowed_users(allowed_roles=['customer']) 
def CustDeliveredOrder(request):
    customer = request.user.customer
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()
    cust = Customer.objects.filter(user=request.user)
    pend = orders.filter(user=request.user, status='Pending')
    ong = orders.filter(user=request.user, status='On Going')
    dlv = orders.filter(user=request.user, status='Delivered')

    context = {
        'customer':customer,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'orders':orders,
        'cust':cust,
        'ongoing':ongoing,
        'pend':pend,
        'ong':ong,
        'dlv':dlv
    }
    return render(request, "customer/delivered_order.html", context)


def UploadSignUp(request):
    customer = Customer.objects.get(user=request.user, is_active=False)
    form = UploadSignUpForm()

    if request.method == 'POST':
        form = UploadSignUpForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            profile_pic = form.cleaned_data.get('profile_pic')
            validid_pic = form.cleaned_data.get('validid_pic')
            faceid_pic = form.cleaned_data.get('faceid_pic')

            customer.user = request.user
            customer.profile_pic = profile_pic
            customer.validid_pic = validid_pic
            customer.faceid_pic = faceid_pic
            customer.save()
            
            messages.info(request, 'Images uploaded!')
            return redirect("/accounts/address/")
            
    context = { 
        'form':form
    } 
    return render(request, "account/upload_sign_up.html", context)

def VerificationSignUp(request):
    customer = Customer.objects.get(user=request.user, is_active=False)
    nme = request.user.customer.first_name

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        customer.complete_address = complete_address
        customer.address_line_2 = address_line_2
        customer.latitude = latitude
        customer.longitude = longitude
        customer.is_active = True
        customer.save()

        messages.info(request, 'Welcome to Sulogoon %s!' % nme)
        return redirect("/signup_success")

    context = { 
        'customer':customer
    } 
    
    return render(request, "account/verification.html", context)

def SuccessSignUp(request):
    customer = Customer.objects.get(user=request.user, is_active=True)

    context = { 
        'customer':customer
    } 
    
    return render(request, "account/success.html", context)


def UserCustomerProfile(request):
    customer = Customer.objects.get(user=request.user, is_active=True)
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    ongoing = orders.filter(status='On Going').count()
    total_orders = orders.count()
    form1 = CustomerForm(instance=customer)
    
    if request.method == 'POST' and 'btnSetting' in request.POST:
        form1 = CustomerForm(request.POST, request.FILES, instance=customer)
        if form1.is_valid():
            form1.save()
            messages.info(request, "Saved!")
            return redirect("core:customer_profile")

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        customer.complete_address = complete_address
        customer.address_line_2 = address_line_2
        customer.latitude = latitude
        customer.longitude = longitude
        customer.save()

    context = {
        'form1':form1,
        'customer':customer,
        'delivered':delivered,
        'pending':pending,
        'ongoing':ongoing,
        'total_orders':total_orders
    }

    return render(request, "customer/user_profile.html", context)

def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request, 'account/password_change.html', context)

def MyAccountCustomer(request):

    context = {
    }

    return render(request, "customer/my_account.html", context)

def EditInfoCustomer(request):
    customer = Customer.objects.get(user=request.user, is_active=True)
    form1 = CustomerForm(instance=customer)
    if request.method == 'POST' and 'btnSetting' in request.POST:
        form1 = CustomerForm(request.POST, request.FILES, instance=customer)
        if form1.is_valid():
            form1.save()
            messages.info(request, "Saved!")
            return redirect("core:customer_edit_information")
        customer.save()

    context = {
        'form1':form1
    }
    return render(request, "customer/edit_info.html", context)

def EditAddressCustomer(request):
    customer = Customer.objects.get(user=request.user, is_active=True)

    if request.method == 'POST' and 'btnAddress' in request.POST:
        complete_address = request.POST['complete_address']
        address_line_2 = request.POST['address_line_2']
        latitude = request.POST['lat1']
        longitude = request.POST['lon1']

        customer.complete_address = complete_address
        customer.address_line_2 = address_line_2
        customer.latitude = latitude
        customer.longitude = longitude
        customer.save()

    context = {
        'customer':customer
    }

    return render(request, "customer/edit_address.html", context)

@login_required
@allowed_users(allowed_roles=['customer']) 
def CustomerOrderHistory(request):
    customer = request.user.customer
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-date_ordered')
    cust = Customer.objects.filter(user=request.user)
    context = {
        'customer':customer,
        'orders':orders,
        'cust':cust,
    }
    return render(request, "customer/order_history.html", context)

@login_required
@allowed_users(allowed_roles=['customer']) 
def CustomerOrderInfo(request, pk):
    orders = Order.objects.get(id=pk)
    order = Order.objects.filter(id=pk)
    rate = Rate.objects.filter(is_active=True)
    context = {
        'orders':orders,
        'order':order,
        'rate':rate
    }
    return render(request, "customer/order_info.html", context)

#def UpdateOrder(request, pk):
#    order = Order.objects.get(id=pk)
#    form = OrderForm(instance=order)
#    mydate = datetime.datetime.now()
#    if request.method == 'POST':
#        form = OrderForm(request.POST, instance=order)
#        if form.is_valid():
#            form.save()
#            order.total = order.get_total_payment()
#            order.save()
#            if order.status == "On Going":
#                order.rider.status = "Unavailable"
#                order.rider.save()
#                order.save()
#            else:
#                order.rider.status = "Available"
#                order.rider.save()
#                order.save()
#            messages.info(request, "Order was successfully updated.")
#            return redirect("core:pending_order")
#    context = {
#        'form':form,
#        'mydate':mydate
#    }
#    return render(request, "admin/update_order.html", context)


#-----------------------------------------------------------------------------------------------------------#
                   ###>>>>>>>>>>>>>>>>>>>>>>> "CUSTOMER END" <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ### 
#-----------------------------------------------------------------------------------------------------------#