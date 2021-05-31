from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

app_name = 'core'
 
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('category/<slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('store/<slug>/', PartnerDetailView.as_view(), name='store'),
    path('contact_us/', Contact_Us, name='contact_us'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('partner_dashboard/', PartnerDashBoard, name='partner_dashboard'),
    path('partner_items/', PartnerItems, name='partner_items'),

    path('shop/', AllCategoryView, name='shop'),
    path('others/', OtherView, name='others'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path('admin_dashboard/', AdminDashBoard, name='admin_dashboard'),
    path('admin_profile/', UserAdminProfile, name='admin_profile'),
    path('pending_order/', PendingOrder, name='admin_pending_order'),
    path('all_categories/', AllCategory, name='all_categories'),
    
    path('items/', AllItems, name='all_items'),
    path('all_order/', AllOrder, name='all_order'),
    path('all_stores/', AllStores, name='all_stores'),
    path('all_admins/', AllAdmins, name='all_admins'),

    path('all_admins/edit/<str:pk>/', EditAdmin, name='edit_admin'),
    path('all_dispatchers/edit/<str:pk>/', EditDispatcher, name='edit_dispatcher'),

    path('all_stores/edit/<str:pk>/', EditPartner, name='edit_store'),
    path('all_customers/edit/<str:pk>/', EditCustomer, name='edit_customer'),
    path('all_dispatchers/', AllDispatchers, name='all_dispatchers'),
    path('all_customers/', AllCustomers, name='all_customers'),
    path('ongoing_order/', OnGoingOrder, name='ongoing_order'),
    path('delivered_order/', DeliveredOrder, name='delivered_order'),
    path('partner/<slug>/', PartnerView.as_view(), name='partner'),
    path('dispatch_dashboard/', DispatchDashBoard, name='dispatch_dashboard'),
    path('customer_dashboard/', CustomerDashBoard, name='customer_dashboard'),

    path('shipping_rate/', ShippingRate, name='shipping_rate'),
 
    path('accounts/upload/', UploadSignUp, name='upload'),
    path('accounts/address/', VerificationSignUp, name='address'),
    path('signup_success/', SuccessSignUp, name='signup_success'),
    path('change_password/', ChangePassword, name='change_password'),
    
    path('dispatch/<str:pk>/', UpdateOrder, name='update_order'),
    path('dispatch_order/<str:pk>/', Dispatch, name='dispatch_order'),
    path('dispatcher_pending_order/', DisPendingOrder, name='dispatcher_pending_order'),
    path('dispatcher_ongoing_order/', DisOnGoingOrder, name='dispatcher_ongoing_order'),
    path('dispatcher_delivered_order/', DisDeliveredOrder, name='dispatcher_delivered_order'),
    path('dispatcher_account_settings/', DispatcherAccountSettings, name='dispatcher_account_settings'),
    path('dispatcher_all_order/', DisAllOrder, name='dispatcher_all_order'),

    path('distance_calculator/', DistanceCalculator, name='distance_calculator'),



    path('partner_profile/', UserPartnerProfile, name='partner_profile'),
    path('partner_pending_order/', PartnerPendingOrder, name='partner_pending_order'),
    path('partner_ongoing_order/', PartnerOnGoingOrder, name='partner_ongoing_order'),
    path('partner_delivered_order/', PartnerDeliveredOrder, name='partner_delivered_order'),

    path('', views.adminsearch, name='adminsearch'),

    ###################################CUSTOMER#########################################
    path('customer_pending_order/', CustPendingOrder, name='customer_pending_order'),
    path('customer/order_history/', CustomerOrderHistory, name='customer_order_history'),
    path('customer/order_information/<str:pk>/', CustomerOrderInfo, name='customer_order_information'),
    path('customer_ongoing_order/', CustOngoingOrder, name='customer_ongoing_order'),
    path('customer_delivered_order/', CustDeliveredOrder, name='customer_delivered_order'),
    path('my_profile/', UserCustomerProfile, name='customer_profile'),
    path('customer/my_account/', MyAccountCustomer, name='customer_my_account'),
    path('customer/edit_information/', EditInfoCustomer, name='customer_edit_information'),
    path('customer/edit_address/', EditAddressCustomer, name='customer_edit_address'),
    ###################################CUSTOMER#########################################

    ###################################RIDER#########################################
    path('all_riders/', AllRiders, name='all_riders'),
    path('all_riders/edit/<str:pk>/', EditRider, name='edit_rider'),
    path('rider_dashboard/', RiderDashBoard, name='rider_dashboard'),
    path('rider_order_status/<str:pk>/', RiderOrderStatus, name='rider_order_status'),
    path('rider_status/', RiderStatus, name='rider_status'),
    path('update_item/<str:pk>', UpdateItem, name='update_item'),
    path('rider_account_settings/', RiderAccountSettings, name='rider_account_settings'),
    path('rider_pending_order/', RidePendingOrder, name='rider_pending_order'),
    path('rider_ongoing_order/', RideOngoingOrder, name='rider_ongoing_order'),
    path('rider_delivered_order/', RideDeliveredOrder, name='rider_delivered_order'),
    
    ###################################RIDER#########################################

    ###################################PARTNERSTORE#########################################

    path('partner_all_order/', PartnerAllOrder, name='partner_all_order'),
    

    ###################################PARTNERSTORE#########################################
]
