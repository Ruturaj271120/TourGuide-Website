from django.contrib import admin
from home.models import Contact,Product,Orders,OrderUpdate,Blogpost

# Register your models here.
admin.site.register(Contact)

admin.site.register(Product)

admin.site.register(Orders)

admin.site.register(OrderUpdate)

admin.site.register(Blogpost)