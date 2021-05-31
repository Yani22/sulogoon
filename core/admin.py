from django.contrib import admin

from .models import *


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'shipping_address',
                    'payment'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'payment'
    ]
    list_filter = ['user',
                   'ordered',]

    search_fields = [
        'user__username',
        'ref_code'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]
    search_fields = ['user',]


def copy_items(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()


copy_items.short_description = 'Copy Items'


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
    ]
    list_filter = ['name', 'is_active']
    search_fields = ['name', 'is_active']
    prepopulated_fields = {"slug": ("name",)}
    actions = [copy_items]

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}

class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active'
    ]
    list_filter = ['title', 'is_active']
    search_fields = ['title', 'is_active']
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Slide)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(BillingAddress, AddressAdmin)
admin.site.register(Rider)
admin.site.register(PartnerStore)
admin.site.register(Customer)
admin.site.register(Dispatcher)
admin.site.register(Other)
admin.site.register(Admin)
admin.site.register(Rate)
admin.site.register(ItemCategory, ItemCategoryAdmin)
