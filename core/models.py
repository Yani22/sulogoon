from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

GENDER_CHOICES= [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ]

SUFFIX_CHOICES= [
    ('Sr', 'Sr.'),
    ('Jr', 'Jr.'),
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VII', 'VII'),
    ('VIII', 'VIII'),
    ('IX', 'IX'),
    ('X', 'X'),
    ('XI', 'XI'),
    ('XII', 'XII'),
    ]
 
class Slide(models.Model):
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class ItemCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class PartnerStore(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    store = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(editable=False, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=4, blank=True, null=True, choices=SUFFIX_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    description_short = models.CharField(max_length=50, blank=True, null=True)
    description_long = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(default="def_prof.jpg")
    validid_pic = models.ImageField(default="def_id.jpg")
    faceid_pic = models.ImageField(default="def_facid.jpeg")
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("core:store", kwargs={
            'slug': self.slug
        })

    def get_absolute_url_admin(self):
        return reverse("core:partner", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        value = self.store
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
        

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(PartnerStore, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    slug = models.SlugField()
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + str(self.name)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    partnerstore = models.ForeignKey(PartnerStore, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    selected_attr = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in {self.partnerstore.store}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('On Going', 'On Going'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    service_charge = models.FloatField(default=0, blank=True, null=True)
    total = models.FloatField(default=0, blank=True, null=True)
    rider = models.ForeignKey(
        'Rider', on_delete=models.SET_NULL, blank=True, null=True)
    partnerstore = models.ForeignKey(
        'PartnerStore', on_delete=models.SET_NULL, blank=True, null=True)
    other = models.ForeignKey(
        'Other', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    surcharge = models.FloatField(default=0, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_payment(self):
        return self.payment.amount + self.service_charge
        

class Other(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    payment_option = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.user)

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True) 
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    kilometer = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=1)

    class Meta:
        verbose_name_plural = 'ShippingAddress'

    def __str__(self):
        return str(self.user)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0)
    payment_choice = models.CharField(max_length=1, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Rider(models.Model):
    STATUS = (
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable')
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=4, blank=True, null=True, choices=SUFFIX_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    profile_pic = models.ImageField(default="def_prof.jpg")
    validid_pic = models.ImageField(default="def_id.jpg")
    faceid_pic = models.ImageField(default="def_facid.jpeg")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=15, null=True, choices=STATUS)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

class Admin(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=4, blank=True, null=True, choices=SUFFIX_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    profile_pic = models.ImageField(default="def_prof.jpg")
    validid_pic = models.ImageField(default="def_id.jpg")
    faceid_pic = models.ImageField(default="def_facid.jpeg")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=4, blank=True, null=True, choices=SUFFIX_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    profile_pic = models.ImageField(default="def_prof.jpg")
    validid_pic = models.ImageField(default="def_id.jpg")
    faceid_pic = models.ImageField(default="def_facid.jpeg")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class Dispatcher(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)   
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    suffix = models.CharField(max_length=4, blank=True, null=True, choices=SUFFIX_CHOICES)
    gender = models.CharField(max_length=6, blank=True, null=True, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    complete_address = models.CharField(max_length=200, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    latitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=6)
    profile_pic = models.ImageField(default="def_prof.jpg")
    validid_pic = models.ImageField(default="def_id.jpg")
    faceid_pic = models.ImageField(default="def_facid.jpeg")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.user)



class Rate(models.Model):
    shipping_rate = models.DecimalField(blank=True, null=True, max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.shipping_rate}"
